"""SSA template generation and explicit checker outcomes."""

from .codegen import generate_verification_templates
from .errors import InvalidInvariantError, SolverExecutionError, SolverTimeoutError
from .models import (
    CandidateRejection,
    LoopStateMaps,
    LoopVerificationInput,
    ProofFailure,
    ProofPhase,
    SolverResult,
    TemplatePaths,
)
from .runner import solve_smt

__all__ = [
    "CandidateRejection",
    "InvalidInvariantError",
    "LoopStateMaps",
    "LoopVerificationInput",
    "ProofFailure",
    "ProofPhase",
    "SolverExecutionError",
    "SolverResult",
    "SolverTimeoutError",
    "TemplatePaths",
    "generate_verification_templates",
    "solve_smt",
]
