"""Verify grouped candidates while sharing support across variable groups."""

import json
from dataclasses import asdict
from itertools import count

from langchain_core.messages import ToolMessage

from nodes.config import read_experiment_options
from nodes.formulas import conjoin_invariants
from nodes.state import WorkflowState
from nodes.verification import verify_candidate_set, verify_invariant


def verify_candidates(state: WorkflowState, config):
    stage = state["per_variable"]
    loop = state["loop"]
    generated_by_variable = stage["candidates"]
    verified_by_variable = stage["verified_invariants"]
    candidates = set().union(*generated_by_variable.values())
    verified = set().union(*verified_by_variable.values())
    generation_round = stage["generation_round"] + 1
    candidate_numbers = count(1)

    def verify(candidate, accepted):
        return verify_invariant(
            config=config,
            invariant=conjoin_invariants(accepted | {candidate}),
            function_name=state["function"]["name"],
            loop_index=loop["index"],
            modified_variables=loop["modified_variables"],
            symbol_names=loop["ssa_states"].before_iteration,
            label=f"per-variable-round_{generation_round}-idx_{next(candidate_numbers)}",
        )

    rejected = verify_candidate_set(
        candidates,
        verified,
        verify,
        fixed_point=read_experiment_options(config).fixed_point_enabled,
    )
    rejections_by_variable = {}
    for variable, generated in generated_by_variable.items():
        generated.intersection_update(candidates)
        verified_by_variable[variable].update(generated & verified)
        pending = [
            rejection for rejection in rejected if rejection.invariant in generated
        ]
        if pending:
            rejections_by_variable[variable] = pending
    stage["has_failures"] = bool(rejections_by_variable)
    stage["rejections"] = rejections_by_variable
    stage["generation_round"] = generation_round if rejections_by_variable else 0
    diagnostic = {
        variable: [asdict(rejection) for rejection in rejections]
        for variable, rejections in rejections_by_variable.items()
    }
    stage["messages"].append(
        ToolMessage(
            content=f"invalid invariants: {json.dumps(diagnostic)}",
            tool_call_id="call_per_variable_candidate_solver",
            name="per_variable_candidate_solver",
        )
    )
    return {"per_variable": stage}
