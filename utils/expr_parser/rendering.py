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
)


class Z3Renderer:
    """Substitute free source variables while preserving quantifier scope."""

    def __init__(self, variable_names=None, *, bound_prefix=""):
        self.variable_names = variable_names or {}
        self.bound_prefix = bound_prefix

    def render(self, expression: Expression, bound_variables=frozenset()) -> str:
        if isinstance(expression, SnapshotVariable):
            return expression.symbol
        if isinstance(expression, Variable):
            if expression.name in bound_variables:
                return self.bound_prefix + expression.name
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
            operand = self.render(expression.operand, bound_variables)
            if expression.operator == "!":
                if expression.c_semantics:
                    operand = f"__as_bool({operand})"
                return f"Not({operand})"
            if expression.c_semantics:
                operand = f"__as_number({operand})"
            return f"({expression.operator}{operand})"
        if isinstance(expression, ArrayAccess):
            array = self.render(expression.array, bound_variables)
            index = self.render(expression.index, bound_variables)
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
                self.bound_prefix + var.name for var in expression.variables
            )
            body = self.render(expression.body, local_variables)
            constructor = "ForAll" if expression.symbol == "∀" else "Exists"
            return f"{constructor}([{variables}], {body})"
        if isinstance(expression, OldExpression):
            raise ValueError("old(...) requires a loop-entry variable mapping")
        raise TypeError(f"Unsupported expression: {type(expression).__name__}")

    def render_binary(self, expression: BinaryExpression, bound_variables) -> str:
        left = self.render(expression.left, bound_variables)
        right = self.render(expression.right, bound_variables)
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
