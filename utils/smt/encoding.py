"""Encode IR statements as SSA constraints under the mathematical-number model."""

from dataclasses import dataclass

from nodes.ir import (
    ArrayAssignment,
    Assignment,
    Assumption,
    BranchCondition,
    Conditional,
    Declaration,
    EnclosingLoopCondition,
    Loop,
    Parameter,
    Statement,
)
from utils.c_types import VAR_ARRAY, VAR_POINTER
from utils.expr_parser.ast import free_variable_names
from utils.expr_parser.parser import parse_expression
from utils.expr_parser.rendering import Z3Renderer
from utils.fol_parser import fol_to_z3, replace_old
from utils.fol_parser.parser import parse_fol

from .models import LoopVerificationInput, SymbolMap


def conjunction(constraints: list[str]) -> str:
    return f"And({', '.join(constraints)})"


def z3_sort_source(c_type: tuple) -> str:
    kind = c_type[0]
    if kind in ("int", "long", "char", "short"):
        return "IntSort()"
    if kind in ("float", "double"):
        return "RealSort()"
    if kind in (VAR_POINTER, VAR_ARRAY):
        return f"ArraySort(IntSort(), {z3_sort_source(c_type[1])})"
    raise NotImplementedError(f"Unsupported C type: {c_type}")


@dataclass
class SsaState:
    """Current versions and declarations; copies isolate alternative paths."""

    versions: dict[str, int]
    declared_variables: set[str]

    @classmethod
    def initial(cls, variable_types) -> "SsaState":
        return cls({name: 0 for name in variable_types}, set())

    def copy(self) -> "SsaState":
        return SsaState(dict(self.versions), set(self.declared_variables))

    def symbol(self, variable: str) -> str:
        return f"{variable}_{self.versions[variable]}"

    @property
    def symbols(self) -> SymbolMap:
        return {name: self.symbol(name) for name in self.versions}

    def fresh_symbol(self, variable: str) -> str:
        self.versions[variable] += 1
        return self.symbol(variable)

    def havoc(self, modified_variables) -> None:
        """Fresh symbols represent an arbitrary iteration or summarized loop exit."""
        for variable in modified_variables:
            self.fresh_symbol(variable)


@dataclass
class EncodedBranch:
    condition: str
    constraints: list[str]
    state: SsaState


class SsaEncoder:
    """Advance SSA state while accumulating source for each statement's constraints."""

    def __init__(self, verification_input: LoopVerificationInput):
        self.variable_types = verification_input.variable_types
        self.loop_invariants = verification_input.loop_invariants
        self.modified_variables_by_loop = verification_input.modified_variables_by_loop
        self.quantified_symbols: set[str] = set()

    def c_expression(self, expression: str, state: SsaState) -> str:
        tree = parse_expression(expression)
        self.require_declared_names(free_variable_names(tree), state)
        return Z3Renderer(state.symbols).render(tree)

    @staticmethod
    def require_declared_names(names: set[str], state: SsaState) -> None:
        undeclared = names - state.declared_variables
        if undeclared:
            raise ValueError(
                f"Undeclared source variables: {', '.join(sorted(undeclared))}"
            )

    def condition(self, expression: str, state: SsaState) -> str:
        return f"__as_bool({self.c_expression(expression, state)})"

    def annotation(self, expression, state: SsaState) -> str:
        tree = parse_fol(expression)
        self.require_declared_names(free_variable_names(tree), state)
        code, binders = fol_to_z3(tree, state.symbols, bound_prefix="__bound_")
        self.quantified_symbols.update(binders)
        return code

    def encode(self, statements: list[Statement], state: SsaState) -> list[str]:
        constraints = []
        for statement in statements:
            constraints.extend(self.encode_statement(statement, state))
        return constraints

    def encode_statement(self, statement: Statement, state: SsaState) -> list[str]:
        if isinstance(statement, Parameter):
            state.declared_variables.add(statement.name)
            return []
        if isinstance(statement, Declaration):
            state.declared_variables.add(statement.name)
            state.fresh_symbol(statement.name)
            return []
        if isinstance(statement, Assignment):
            return [self.encode_assignment(statement, state)]
        if isinstance(statement, ArrayAssignment):
            return [self.encode_array_assignment(statement, state)]
        if isinstance(statement, EnclosingLoopCondition):
            return self.encode_enclosing_loop(statement, state)
        if isinstance(statement, BranchCondition):
            return [self.condition(statement.expression, state)]
        if isinstance(statement, Assumption):
            return [self.annotation(statement.expression, state)]
        if isinstance(statement, Loop):
            return self.encode_loop_summary(statement, state)
        if isinstance(statement, Conditional):
            return [self.encode_conditional(statement, state)]
        raise NotImplementedError(f"Unsupported IR statement: {statement}")

    @staticmethod
    def assignment_value(value: str, target_type: tuple) -> str:
        """C real-to-integer assignment truncates toward zero, including array stores."""
        kind = target_type[0]
        if kind in ("int", "long", "char", "short"):
            return f"__to_int({value})"
        if kind in ("float", "double"):
            return f"__as_number({value})"
        return value

    def encode_assignment(self, statement: Assignment, state: SsaState) -> str:
        self.require_declared_names({statement.target}, state)
        value = self.c_expression(statement.value, state)
        value = self.assignment_value(value, self.variable_types[statement.target])
        target = state.fresh_symbol(statement.target)
        return f"{target} == {value}"

    def encode_array_assignment(
        self, statement: ArrayAssignment, state: SsaState
    ) -> str:
        self.require_declared_names({statement.array_name}, state)
        # Read the array, index and value before advancing the array's version.
        old_array = state.symbol(statement.array_name)
        index = f"__as_number({self.c_expression(statement.index, state)})"
        value = self.c_expression(statement.value, state)
        element_type = self.variable_types[statement.array_name][1]
        value = self.assignment_value(value, element_type)
        new_array = state.fresh_symbol(statement.array_name)
        return f"{new_array} == Store({old_array}, {index}, {value})"

    def encode_invariants(
        self, invariants, entry: SsaState, current: SsaState
    ) -> list[str]:
        constraints = []
        for invariant in sorted(invariants):
            resolved = replace_old(invariant, entry.versions, entry.declared_variables)
            constraints.append(self.annotation(resolved, current))
        return constraints

    def encode_enclosing_loop(
        self, statement: EnclosingLoopCondition, state: SsaState
    ) -> list[str]:
        """An unknown enclosing invariant contributes only havoc and its guard."""
        entry = state.copy()
        state.havoc(self.modified_variables_by_loop[statement.loop_id])
        invariants = (
            self.loop_invariants[statement.loop_id]
            if statement.loop_id < len(self.loop_invariants)
            else set()
        )
        constraints = self.encode_invariants(invariants, entry, state)
        constraints.append(self.condition(statement.expression, state))
        return constraints

    def encode_loop_summary(self, loop: Loop, state: SsaState) -> list[str]:
        """Replace an already checked loop by its invariant and exit condition."""
        entry = state.copy()
        state.havoc(self.modified_variables_by_loop[loop.loop_id])
        constraints = self.encode_invariants(
            self.loop_invariants[loop.loop_id], entry, state
        )
        constraints.append(f"Not({self.condition(loop.condition, state)})")
        return constraints

    def encode_conditional(self, statement: Conditional, state: SsaState) -> str:
        branches = []
        for condition, statements in statement.branches:
            branch_state = state.copy()
            condition_code = self.condition(condition, state)
            constraints = self.encode(statements, branch_state)
            branches.append(EncodedBranch(condition_code, constraints, branch_state))

        # Each alternative must define the same final version for every variable.
        for variable in state.versions:
            state.versions[variable] = max(
                branch.state.versions[variable] for branch in branches
            )
        alternatives = []
        for branch in branches:
            for variable, final_version in state.versions.items():
                if branch.state.versions[variable] != final_version:
                    branch.constraints.append(
                        f"{state.symbol(variable)} == {branch.state.symbol(variable)}"
                    )
            alternatives.append(conjunction([branch.condition, *branch.constraints]))
        return f"Or({', '.join(alternatives)})"

    def declarations(self, state: SsaState) -> str:
        lines = []
        for variable, c_type in self.variable_types.items():
            for version in range(state.versions[variable] + 1):
                symbol = f"{variable}_{version}"
                lines.append(f'{symbol} = Const("{symbol}", {z3_sort_source(c_type)})')
        for binder in sorted(self.quantified_symbols):
            lines.append(f'{binder} = Int("{binder}")')
        return "\n".join(lines)
