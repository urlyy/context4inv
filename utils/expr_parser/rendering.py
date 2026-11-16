"""Render parsed expressions as Python source for the generated Z3 checker."""

from .ast import (
    ArrayAccess,
    BinaryExpression,
    BooleanLiteral,
    Expression,
    NumberLiteral,
    OldExpression,
    Quantifier,
    SnapshotVariable,
    UnaryExpression,
    Variable,
    bound_variable_names,
    free_variable_names,
    walk_expression,
)


class Z3Renderer:
    """Substitute free source variables while preserving quantifier scope."""

    def __init__(self, variable_names=None, *, bound_prefix=""):
        self.variable_names = variable_names or {}
        self.bound_prefix = bound_prefix
        self.bound_symbols: dict[str, str] = {}

    @property
    def quantified_symbols(self) -> set[str]:
        return set(self.bound_symbols.values())

    def render(self, expression: Expression) -> str:
        """Allocate bound symbols away from free variables and checker names."""
        used_names = set(self.variable_names.values())
        used_names |= free_variable_names(expression)
        used_names.update(
            node.symbol
            for node in walk_expression(expression)
            if isinstance(node, SnapshotVariable)
        )
        self.bound_symbols = {}
        for variable in sorted(bound_variable_names(expression)):
            # SSA symbols end in a numeric version. A nonnumeric suffix also
            # avoids collisions with versions introduced by a later formula.
            symbol = self.bound_prefix + variable + "_q"
            while symbol in used_names:
                symbol += "_q"
            self.bound_symbols[variable] = symbol
            used_names.add(symbol)
        return self._render(expression, frozenset())

    def _render(self, expression: Expression, bound_variables) -> str:
        if isinstance(expression, SnapshotVariable):
            return expression.symbol
        if isinstance(expression, Variable):
            if expression.name in bound_variables:
                return self.bound_symbols[expression.name]
            return self.variable_names.get(expression.name, expression.name)
        if isinstance(expression, NumberLiteral):
            constructor = (
                "RealVal"
                if any(char in expression.text for char in ".eE")
                else "IntVal"
            )
            return f'{constructor}("{expression.text}")'
        if isinstance(expression, BooleanLiteral):
            return f"BoolVal({expression.value})"
        if isinstance(expression, UnaryExpression):
            operand = self._render(expression.operand, bound_variables)
            if expression.operator == "!":
                if expression.c_semantics:
                    operand = f"__as_bool({operand})"
                return f"Not({operand})"
            if expression.c_semantics:
                operand = f"__as_number({operand})"
            return f"({expression.operator}{operand})"
        if isinstance(expression, ArrayAccess):
            array = self._render(expression.array, bound_variables)
            index = self._render(expression.index, bound_variables)
            if expression.c_semantics:
                index = f"__as_number({index})"
            return f"Select({array}, {index})"
        if isinstance(expression, BinaryExpression):
            return self.render_binary(expression, bound_variables)
        if isinstance(expression, Quantifier):
            local_variables = bound_variables | {
                var.name for var in expression.variables
            }
            variables = ", ".join(
                self.bound_symbols[var.name] for var in expression.variables
            )
            body = self._render(expression.body, local_variables)
            constructor = "ForAll" if expression.symbol == "∀" else "Exists"
            return f"{constructor}([{variables}], {body})"
        if isinstance(expression, OldExpression):
            raise ValueError("old(...) requires a loop-entry variable mapping")
        raise TypeError(f"Unsupported expression: {type(expression).__name__}")

    def render_binary(self, expression: BinaryExpression, bound_variables) -> str:
        left = self._render(expression.left, bound_variables)
        right = self._render(expression.right, bound_variables)
        logical_function = {"&&": "And", "||": "Or", "=>": "Implies"}.get(
            expression.operator
        )
        if logical_function:
            if expression.c_semantics:
                left, right = f"__as_bool({left})", f"__as_bool({right})"
            return f"{logical_function}({left}, {right})"
        if expression.c_semantics:
            left, right = f"__as_number({left})", f"__as_number({right})"
        return f"({left} {expression.operator} {right})"
