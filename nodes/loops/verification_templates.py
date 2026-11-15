"""Connect workflow state to the SMT template generator."""

from nodes.artifacts import invariant_template_path, postcondition_template_path
from nodes.state import WorkflowState
from utils.smt import (
    LoopVerificationInput,
    TemplatePaths,
    generate_verification_templates,
)


def prepare_verification_templates(state: WorkflowState, config) -> WorkflowState:
    loop = state["loop"]
    function = state["function"]
    verification = LoopVerificationInput(
        path=loop["path"],
        variable_types=function["variable_types"],
        loop_invariants=function["loop_invariants"],
        modified_variables_by_loop=function["modified_variables_by_loop"],
    )
    paths = TemplatePaths(
        invariant=invariant_template_path(config, function["name"], loop["index"]),
        postcondition=postcondition_template_path(
            config, function["name"], loop["index"]
        ),
    )
    ssa_states = generate_verification_templates(verification, paths)
    loop["ssa_states"] = ssa_states
    function["ssa_states_by_loop"].append(ssa_states)
    return {"loop": loop, "function": function}
