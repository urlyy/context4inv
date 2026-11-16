"""Resolve old(expr) against loop-entry symbols without serializing the AST."""

from utils.expr_parser.ast import (
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
    walk_expression,
)

from .parser import parse_fol


class LoopEntryResolver:
    """Keep bound variables local; freeze only free variables inside old(expr)."""

    def __init__(
        self,
        expression: Expression,
        entry_symbols: dict[str, str],
        *,
        complete_entry_state=False,
    ):
        self.entry_symbols = entry_symbols
        self.complete_entry_state = complete_entry_state
        self.used_names = set(entry_symbols) | set(entry_symbols.values())
        for node in walk_expression(expression):
            if isinstance(node, Variable):
                self.used_names.add(node.name)
            elif isinstance(node, SnapshotVariable):
                self.used_names.add(node.symbol)

    def fresh_bound_name(self) -> str:
        index = len(self.used_names)
        while (name := f"__old_bound_{index}") in self.used_names:
            index += 1
        self.used_names.add(name)
        return name

    def resolve(
        self, expression: Expression, bound_names=None, *, at_entry=False
    ) -> Expression:
        bound_names = bound_names or {}
        if isinstance(expression, SnapshotVariable):
            return expression
        if isinstance(expression, Variable):
            if expression.name in bound_names:
                return Variable(bound_names[expression.name])
            if at_entry and expression.name in self.entry_symbols:
                return SnapshotVariable(self.entry_symbols[expression.name])
            if at_entry and self.complete_entry_state:
                raise ValueError(f"No loop-entry value for variable: {expression.name}")
            return expression
        if isinstance(expression, (NumberLiteral, BooleanLiteral)):
            return expression
        if isinstance(expression, OldExpression):
            return self.resolve(expression.operand, bound_names, at_entry=True)
        if isinstance(expression, UnaryExpression):
            operand = self.resolve(expression.operand, bound_names, at_entry=at_entry)
            return UnaryExpression(expression.operator, operand, expression.c_semantics)
        if isinstance(expression, ArrayAccess):
            return ArrayAccess(
                self.resolve(expression.array, bound_names, at_entry=at_entry),
                self.resolve(expression.index, bound_names, at_entry=at_entry),
                expression.c_semantics,
            )
        if isinstance(expression, BinaryExpression):
            return BinaryExpression(
                self.resolve(expression.left, bound_names, at_entry=at_entry),
                expression.operator,
                self.resolve(expression.right, bound_names, at_entry=at_entry),
                expression.c_semantics,
            )
        if isinstance(expression, Quantifier):
            return self.resolve_quantifier(expression, bound_names, at_entry=at_entry)
        raise TypeError(f"Unsupported annotation: {type(expression).__name__}")

    def resolve_quantifier(
        self, expression: Quantifier, bound_names, *, at_entry
    ) -> Quantifier:
        # Alpha-renaming prevents a generated snapshot name from becoming bound.
        local_names = {
            variable.name: self.fresh_bound_name() for variable in expression.variables
        }
        body = self.resolve(
            expression.body, bound_names | local_names, at_entry=at_entry
        )
        variables = tuple(Variable(name) for name in local_names.values())
        return Quantifier(expression.symbol, variables, body)


def resolve_entry_symbols(expression, entry_symbols, *, complete_entry_state=False):
    tree = parse_fol(expression)
    return LoopEntryResolver(
        tree, entry_symbols, complete_entry_state=complete_entry_state
    ).resolve(tree)


def replace_old(expression, old_counter, declared_vars):
    """Bind old(expr) to the state before this particular loop invocation."""
    symbols = {
        name: f"{name}_{old_counter[name]}"
        for name in declared_vars
        if name in old_counter
    }
    return resolve_entry_symbols(expression, symbols, complete_entry_state=True)


def replace_old_for_solve(expression, key_vars):
    """Bind old(modified_var) to the candidate checker's fixed entry parameter."""
    symbols = {name: f"__entry_values[{name!r}]" for name in key_vars}
    return resolve_entry_symbols(expression, symbols)
