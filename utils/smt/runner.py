"""Run self-contained checker artifacts and decode their explicit exit protocol."""

import json
import subprocess
import sys
import time
from pathlib import Path

from utils.python_format import format_py

from .errors import InvalidInvariantError, SolverExecutionError, SolverTimeoutError
from .models import SOLVER_TIMEOUT_SECONDS, ProofFailure, ProofPhase, SolverResult
from .protocol import COUNTEREXAMPLE_EXIT, INVALID_INVARIANT_EXIT, UNKNOWN_EXIT


def read_diagnostic(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise SolverExecutionError(
            f"Invalid checker diagnostic {path}: {error}"
        ) from error


def candidate_diagnostic(data: dict) -> str:
    if data["kind"] != "invalid_invariant":
        raise ValueError("Unexpected checker diagnostic kind")
    return f"{data['error_type']}: {data['message']}"


def proof_failure(exit_code: int, data: dict) -> ProofFailure:
    phase = ProofPhase(data["reason"])
    if exit_code == UNKNOWN_EXIT:
        return ProofFailure(phase=phase, unknown_reason=data["unknown_reason"])
    return ProofFailure(phase=phase, counterexample=data["counterexample"])


def decode_result(
    process, diagnostic_path: Path, elapsed_seconds: float
) -> SolverResult:
    if process.returncode == 0:
        return SolverResult(valid=True, failure=None, elapsed_seconds=elapsed_seconds)

    if process.returncode in (
        COUNTEREXAMPLE_EXIT,
        UNKNOWN_EXIT,
        INVALID_INVARIANT_EXIT,
    ):
        data = read_diagnostic(diagnostic_path)
        try:
            if process.returncode == INVALID_INVARIANT_EXIT:
                rejection_reason = candidate_diagnostic(data)
                failure = None
            else:
                failure = proof_failure(process.returncode, data)
                rejection_reason = None
        except (ValueError, KeyError) as error:
            raise SolverExecutionError(
                f"Invalid checker diagnostic {diagnostic_path}: {error}"
            ) from error
        if rejection_reason is not None:
            raise InvalidInvariantError(rejection_reason)
        return SolverResult(
            valid=False, failure=failure, elapsed_seconds=elapsed_seconds
        )

    raise SolverExecutionError(
        f"Checker exited with code {process.returncode}: {diagnostic_path}\n"
        f"{process.stderr or process.stdout}"
    )


def solve_smt(checker_file: str | Path) -> SolverResult:
    """Run with this interpreter; candidate errors never become proof failures."""
    path = Path(checker_file).resolve()
    diagnostic = format_py(path)
    if diagnostic is not None:
        raise SolverExecutionError(f"Invalid checker {path}: {diagnostic}")

    diagnostic_path = path.with_name(f"{path.stem}_counterexample.json")
    diagnostic_path.unlink(missing_ok=True)
    start = time.perf_counter()
    try:
        process = subprocess.run(
            [sys.executable, str(path), str(diagnostic_path)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=SOLVER_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as error:
        raise SolverTimeoutError(
            f"Checker exceeded {SOLVER_TIMEOUT_SECONDS}s: {path}"
        ) from error
    elapsed_seconds = time.perf_counter() - start
    return decode_result(process, diagnostic_path, elapsed_seconds)
