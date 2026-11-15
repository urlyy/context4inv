"""Combine invariants and compile their source names into Z3 expressions."""

from collections.abc import Iterable
from dataclasses import dataclass

from utils.fol_parser import fol_to_z3


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
    """Keep modified variables as checker parameters; capture stable SSA symbols.

    Variables quantified by the invariant receive separate symbols. old() must
    already have been resolved against the target loop's entry snapshot.
    """
    parameter_names = {
        variable: variable if variable in modified_variables else ssa_symbol
        for variable, ssa_symbol in ssa_names.items()
    }
    expression, quantified_variables = fol_to_z3(
        invariant, parameter_names, bound_prefix="__bound_"
    )
    variable_names = sorted(quantified_variables)
    bindings = ""
    if variable_names:
        assignment = ", ".join(variable_names)
        if len(variable_names) == 1:
            assignment += ","
        bindings = f'{assignment} = Ints("{" ".join(variable_names)}")'
    return InvariantExpression(bindings=bindings, expression=expression)
