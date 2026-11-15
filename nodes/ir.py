"""Statement types produced by C parsing and consumed by SSA encoding."""

from dataclasses import dataclass, field


class Statement:
    """Base type for the supported verification language."""


@dataclass
class Assumption(Statement):
    expression: str


@dataclass
class Assertion(Statement):
    expression: str


@dataclass
class Declaration(Statement):
    """A local declaration introduces a fresh, initially unconstrained value."""

    name: str


@dataclass
class Parameter(Statement):
    """A function parameter is an unconstrained input, declared once at entry."""

    name: str


@dataclass
class Assignment(Statement):
    target: str
    value: str


@dataclass
class ArrayAssignment(Statement):
    array_name: str
    index: str
    value: str


@dataclass
class Conditional(Statement):
    """Mutually exclusive branches, each containing a condition and its statements."""

    branches: list[tuple[str, list[Statement]]]


@dataclass
class BranchCondition(Statement):
    """A condition that holds on the selected path to a loop."""

    expression: str


@dataclass
class EnclosingLoopCondition(Statement):
    """Entry into an arbitrary iteration of an enclosing loop."""

    expression: str
    loop_id: int


@dataclass
class Loop(Statement):
    """A loop head, one iteration, and the statements leading to its assertion.

    The initializer belongs to the preceding path. The body includes a for-loop's
    update, and loop_id follows verification order: inner loops precede outer ones.
    """

    condition: str
    body: list[Statement]
    depth: int
    loop_id: int
    postcondition: str | None
    variable_dependencies: dict[str, set[str]]
    post_statements: list[Statement] = field(default_factory=list)
