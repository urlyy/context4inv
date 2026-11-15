"""Immutable syntax nodes shared by C expressions and logical annotations.

C expression nodes request scalar Boolean/numeric promotion when rendered.
Annotations keep mathematical Boolean logic. Number literals retain their exact
source text, so parsing never rounds a decimal through Python float.
"""

from collections.abc import Iterator
from dataclasses import dataclass


class Expression:
    pass


@dataclass(frozen=True)
class Variable(Expression):
    name: str


@dataclass(frozen=True)
class SnapshotVariable(Expression):
    """A resolved loop-entry symbol; source-name substitution must skip it."""

    symbol: str


@dataclass(frozen=True)
class NumberLiteral(Expression):
    text: str


@dataclass(frozen=True)
class BooleanLiteral(Expression):
    value: bool


@dataclass(frozen=True)
class UnaryExpression(Expression):
    operator: str
    operand: Expression
    c_semantics: bool = False


@dataclass(frozen=True)
class BinaryExpression(Expression):
    left: Expression
    operator: str
    right: Expression
    c_semantics: bool = False


@dataclass(frozen=True)
class ArrayAccess(Expression):
    array: Expression
    index: Expression
    c_semantics: bool = False


@dataclass(frozen=True)
class Quantifier(Expression):
    symbol: str
    variables: tuple[Variable, ...]
    body: Expression


@dataclass(frozen=True)
class OldExpression(Expression):
    operand: Expression


def child_expressions(expression: Expression) -> tuple[Expression, ...]:
    if isinstance(expression, (UnaryExpression, OldExpression)):
        return (expression.operand,)
    if isinstance(expression, BinaryExpression):
        return expression.left, expression.right
    if isinstance(expression, ArrayAccess):
        return expression.array, expression.index
    if isinstance(expression, Quantifier):
        return (*expression.variables, expression.body)
    return ()


def walk_expression(expression: Expression) -> Iterator[Expression]:
    """Visit syntax nodes without recursing through long conjunctions."""
    pending = [expression]
    while pending:
        current = pending.pop()
        yield current
        pending.extend(reversed(child_expressions(current)))


def bound_variable_names(expression: Expression) -> set[str]:
    return {
        variable.name
        for node in walk_expression(expression)
        if isinstance(node, Quantifier)
        for variable in node.variables
    }
