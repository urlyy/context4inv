"""Check added constraints and retain their diagnostics for the next request."""

from nodes.feedback import remember_rejections
from nodes.state import WorkflowState
from nodes.verification import verify_stage_candidates


def verify_candidates(state: WorkflowState, config):
    generated = set(state["postcondition"]["candidates"])
    result = verify_stage_candidates(
        state, config, "postcondition", advance_round=False
    )
    stage = result["postcondition"]
    remember_rejections(
        stage.setdefault("candidate_rejections", {}),
        stage["rejections"],
        stage["verified_invariants"],
    )
    invalid = set(stage.get("invalid_candidates", ())) | (
        generated - stage["candidates"]
    )
    stage["invalid_candidates"] = sorted(invalid - stage["verified_invariants"])
    return result
