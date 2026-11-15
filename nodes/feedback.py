"""Format solver diagnostics with source names and loop-local entry snapshots."""

import re

from utils.smt.models import CandidateRejection, LoopStateMaps, ProofFailure, ProofPhase

_PHASE_LABELS = {
    ProofPhase.INITIALIZATION: "initialization at loop entry",
    ProofPhase.PRESERVATION: "preservation across one iteration",
    ProofPhase.POSTCONDITION: "postcondition at loop exit",
}


def markdown_table(headers: list[str], rows: list[tuple]) -> str:
    def row(values):
        return "| " + " | ".join(map(str, values)) + " |"

    return "\n".join([row(headers), row(["---"] * len(headers)), *map(row, rows)])


def format_counterexample(
    invariant, variables, failure: ProofFailure, states: LoopStateMaps
) -> str:
    """Show exactly the states involved in the failed obligation."""
    phase = failure.phase
    headers = {
        ProofPhase.INITIALIZATION: ["variable", "value_at_loop_entry"],
        ProofPhase.PRESERVATION: [
            "variable",
            "value_before_iteration",
            "value_after_iteration",
        ],
        ProofPhase.POSTCONDITION: ["variable", "value_at_loop_exit"],
    }[phase]
    current = {
        ProofPhase.INITIALIZATION: states.entry,
        ProofPhase.PRESERVATION: states.before_iteration,
        ProofPhase.POSTCONDITION: states.exit,
    }[phase]
    show_entry = (
        phase != ProofPhase.INITIALIZATION
        and re.search(r"\bold\s*\(", invariant) is not None
    )
    if show_entry:
        headers.insert(1, "value_at_loop_entry (old)")
    values = failure.counterexample
    rows = []
    for variable, symbol in current.items():
        if variable not in variables and not re.search(
            rf"\b{re.escape(variable)}\b", invariant
        ):
            continue
        symbols = [symbol]
        if phase == ProofPhase.PRESERVATION:
            symbols.append(states.after_iteration[variable])
        if show_entry:
            symbols.insert(0, states.entry[variable])
        if all(symbol in values for symbol in symbols):
            rows.append((variable, *(values[symbol] for symbol in symbols)))
    return markdown_table(headers, rows) + "\n"


def format_solver_diagnostic(
    invariant, failure: ProofFailure, variables, states: LoopStateMaps
) -> str:
    if failure.is_unknown:
        return f"Verification is inconclusive: Z3 returned unknown ({failure.unknown_reason}).\n"
    return "The counterexample is:\n" + format_counterexample(
        invariant, variables, failure, states
    )


def format_generation_rejections(rejections, variables, states: LoopStateMaps) -> str:
    """Format initial-generation feedback without repeating candidate lookups."""
    sections = []
    for rejection in rejections:
        failure = rejection.failure
        detail = f"- `{rejection.invariant}`. "
        if failure.is_unknown:
            detail += f"The result of the Z3 solver is `unknown` due to `{failure.unknown_reason}`."
        else:
            detail += "A counterexample:\n" + format_counterexample(
                rejection.invariant, variables, failure, states
            )
        sections.append(detail + "\n")
    return "".join(sections)


def format_candidate_rejections(
    rejections, invalid_candidates, loop_name, variables, states: LoopStateMaps
) -> str:
    sections = []
    for rejection in sorted(rejections, key=lambda item: item.invariant):
        sections.append(
            f"- `{rejection.invariant}` for `{loop_name}`: {_PHASE_LABELS[rejection.failure.phase]}.\n"
            + format_solver_diagnostic(
                rejection.invariant, rejection.failure, variables, states
            )
        )
    for invariant in sorted(invalid_candidates):
        sections.append(
            f"- `{invariant}` for `{loop_name}`: rejected as a malformed or incorrectly typed Boolean formula; no semantic counterexample was produced.\n"
        )
    if not sections:
        return ""
    return (
        "Rejected candidate diagnostics (from their most recent checks):\n"
        + "\n".join(sections)
        + "\nThese candidates were not added to the verified set. Address the indicated failure phase and values. Do not repeat a disproven formula unchanged unless strengthened prerequisites or earlier-loop summaries resolve its recorded failure. An initialization failure occurs before any loop iteration, even when an inner loop will later initialize its own counter.\n"
    )


def remember_rejections(
    previous: dict[str, CandidateRejection], rejected, accepted
) -> None:
    """Keep each formula's latest diagnostic, removing formulas subsequently proved."""
    previous.update((rejection.invariant, rejection) for rejection in rejected)
    for invariant in accepted:
        previous.pop(invariant, None)
