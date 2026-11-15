from nodes.state import WorkflowState
from nodes.verification import verify_stage_candidates


def verify_candidates(state: WorkflowState, config):
    return verify_stage_candidates(state, config, "combined")
