"""Execute invariant checks and grow verified candidates to a fixed point."""

import json
from dataclasses import asdict
from itertools import count

from langchain_core.messages import ToolMessage
from pyparsing import ParseBaseException

from nodes.artifacts import (
    error_log_path,
    invariant_template_path,
    postcondition_template_path,
    verification_directory,
)
from nodes.config import read_experiment_options
from nodes.formulas import compile_invariant, conjoin_invariants
from utils.fol_parser import replace_old_for_solve
from utils.smt import InvalidInvariantError, solve_smt
from utils.smt.models import CandidateRejection, SolverResult


def _record_invalid_formula(config, function_name, loop_index, invariant, error):
    with error_log_path(config, function_name, loop_index).open(
        "a", encoding="utf-8"
    ) as stream:
        stream.write(f"Invalid invariant {invariant!r}: {error}\n")


def verify_invariant(
    config,
    invariant,
    function_name,
    loop_index,
    modified_variables,
    symbol_names,
    *,
    label,
    postcondition=False,
) -> SolverResult | None:
    """Return None only for malformed or incorrectly typed candidate formulas."""
    try:
        formula = replace_old_for_solve(invariant, modified_variables)
        candidate = compile_invariant(formula, modified_variables, symbol_names)
    except (ParseBaseException, ValueError) as error:
        _record_invalid_formula(config, function_name, loop_index, invariant, error)
        return None
    template_path = (
        postcondition_template_path if postcondition else invariant_template_path
    )
    template = template_path(config, function_name, loop_index).read_text(
        encoding="utf-8"
    )
    checker = verification_directory(config, function_name, loop_index) / f"{label}.py"
    checker.write_text(
        template.format(
            candidate_bindings=candidate.bindings,
            candidate_description=" ".join(invariant.splitlines()),
            candidate_expression=candidate.expression,
        ),
        encoding="utf-8",
    )
    try:
        return solve_smt(checker)
    except InvalidInvariantError as error:
        _record_invalid_formula(config, function_name, loop_index, invariant, error)
        return None


def verify_candidate_set(candidates, verified_invariants, verify, *, fixed_point=True):
    """Recheck pending candidates when another invariant strengthens the hypothesis.

    A formula can fail preservation alone and become provable once another
    candidate has been established. The verified set only grows. Another pass
    is useful only after that growth; stale counterexamples are removed when
    their formulas become provable. Disabling fixed_point keeps one pass.
    """
    rejections = {}
    while True:
        found_invariant = False
        for invariant in sorted(candidates - verified_invariants):
            result = verify(invariant, verified_invariants)
            if result is None:
                candidates.remove(invariant)
                rejections.pop(invariant, None)
            elif result.valid:
                verified_invariants.add(invariant)
                rejections.pop(invariant, None)
                found_invariant = True
            else:
                rejections[invariant] = CandidateRejection(invariant, result.failure)
        if not found_invariant or not fixed_point:
            return list(rejections.values())


def verify_stage_candidates(state, config, stage_name, *, advance_round=True):
    """Check a set-valued stage while its caller owns generation-round policy."""
    stage = state[stage_name]
    loop = state["loop"]
    generation_round = stage["generation_round"] + int(advance_round)
    candidate_numbers = count(1)

    def verify(candidate, accepted):
        return verify_invariant(
            config=config,
            invariant=conjoin_invariants(accepted | {candidate}),
            function_name=state["function"]["name"],
            loop_index=loop["index"],
            modified_variables=loop["modified_variables"],
            symbol_names=loop["ssa_states"].before_iteration,
            label=f"{stage_name}-candidates-round_{generation_round}-idx_{next(candidate_numbers)}",
        )

    rejections = verify_candidate_set(
        stage["candidates"],
        stage["verified_invariants"],
        verify,
        fixed_point=read_experiment_options(config).fixed_point_enabled,
    )
    stage["has_failures"] = bool(rejections)
    stage["rejections"] = rejections
    if advance_round:
        stage["generation_round"] = generation_round if rejections else 0
    stage["messages"].append(
        ToolMessage(
            content=f"invalid invariants: {json.dumps([asdict(item) for item in rejections])}",
            tool_call_id=f"call_{stage_name}_candidate_solver",
            name=f"{stage_name}_candidate_solver",
        )
    )
    return {stage_name: stage}
