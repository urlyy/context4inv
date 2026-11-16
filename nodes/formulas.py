"""Combine invariants and compile their source names into Z3 expressions."""

from collections.abc import Iterable
from dataclasses import dataclass

from utils.expr_parser.ast import free_variable_names
from utils.fol_parser import fol_to_z3
from utils.fol_parser.parser import parse_fol


@dataclass(frozen=True)
class InvariantExpression:
    """Declarations for quantified variables and the Boolean checker expression."""

    bindings: str
    expression: str


def conjoin_invariants(invariants: Iterable[str]) -> str:
    return " && ".join(f"({invariant})" for invariant in sorted(invariants))


def compile_invariant(
    invariant, modified_variables: list[str], ssa_names: dict[str, str]
) -> InvariantExpression:
    """Read modified variables from checker arguments; capture stable SSA symbols.

    Variables quantified by the invariant receive separate symbols. old() must
    already have been resolved against the target loop's entry snapshot.
    """
    tree = parse_fol(invariant)
    unknown_variables = free_variable_names(tree) - ssa_names.keys()
    if unknown_variables:
        raise ValueError(
            f"Undeclared invariant variables: {', '.join(sorted(unknown_variables))}"
        )
    parameter_names = {
        variable: f"__current_values[{variable!r}]"
        if variable in modified_variables
        else ssa_symbol
        for variable, ssa_symbol in ssa_names.items()
    }
    expression, quantified_variables = fol_to_z3(
        tree, parameter_names, bound_prefix="__bound_"
    )
    variable_names = sorted(quantified_variables)
    bindings = ""
    if variable_names:
        assignment = ", ".join(variable_names)
        if len(variable_names) == 1:
            assignment += ","
        bindings = f'{assignment} = Ints("{" ".join(variable_names)}")'
    return InvariantExpression(bindings=bindings, expression=expression)
