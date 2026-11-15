"""Named inputs, SSA snapshots and results shared by verification stages."""

from dataclasses import dataclass
from enum import IntEnum
from pathlib import Path
from typing import cast

from nodes.ir import Loop, Statement
from utils.c_types import CType

SOLVER_TIMEOUT_SECONDS = 10

SymbolMap = dict[str, str]


class ProofPhase(IntEnum):
    """The three partial-correctness obligations, in execution order."""

    INITIALIZATION = 0
    PRESERVATION = 1
    POSTCONDITION = 2


@dataclass(frozen=True)
class LoopVerificationInput:
    """The path ends in the target loop; earlier loops use verified summaries."""

    path: list[Statement]
    variable_types: dict[str, CType]
    loop_invariants: list[set[str]]
    modified_variables_by_loop: list[list[str]]

    @property
    def loop(self) -> Loop:
        return cast(Loop, self.path[-1])

    @property
    def modified_variables(self) -> list[str]:
        return sorted(self.modified_variables_by_loop[self.loop.loop_id])


@dataclass(frozen=True)
class TemplatePaths:
    invariant: Path
    postcondition: Path


@dataclass(frozen=True)
class LoopStateMaps:
    """Exit denotes the loop exit, before statements leading to the assertion."""

    entry: SymbolMap
    before_iteration: SymbolMap
    after_iteration: SymbolMap
    exit: SymbolMap


@dataclass(frozen=True)
class ProofFailure:
    """A real counterexample or an inconclusive solver result, never a bad candidate."""

    phase: ProofPhase
    counterexample: dict[str, str] | None = None
    unknown_reason: str | None = None

    @property
    def is_unknown(self) -> bool:
        return self.unknown_reason is not None


@dataclass(frozen=True)
class CandidateRejection:
    invariant: str
    failure: ProofFailure


@dataclass(frozen=True)
class SolverResult:
    valid: bool
    failure: ProofFailure | None
    elapsed_seconds: float
