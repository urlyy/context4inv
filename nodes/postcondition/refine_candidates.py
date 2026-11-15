from langchain_core.messages import HumanMessage

from nodes.feedback import format_candidate_rejections, format_solver_diagnostic
from nodes.formulas import conjoin_invariants
from nodes.generation import request_stage_candidates
from nodes.state import WorkflowState
from prompt_templates import postcondition_refinement_prompt


def refine_candidates(state: WorkflowState, config):
    stage = state["postcondition"]
    loop = state["loop"]
    verified = stage["verified_invariants"]
    diagnostic = format_solver_diagnostic(
        conjoin_invariants(verified),
        stage["failure"],
        loop["counterexample_variables"],
        loop["ssa_states"],
    )
    diagnostic += "\n" + format_candidate_rejections(
        stage.get("candidate_rejections", {}).values(),
        stage.get("invalid_candidates", ()),
        f"LOOP_{loop['index']}",
        loop["counterexample_variables"],
        loop["ssa_states"],
    )
    user_message = HumanMessage(
        content=postcondition_refinement_prompt.format(
            loop_name=f"LOOP_{loop['index']}",
            invariants=verified,
            fail_reason=diagnostic,
        )
    )
    stage["messages"].append(user_message)
    messages = [
        state["program"]["formula_rules_message"],
        loop["code_message"],
        stage["format_message"],
        user_message,
    ]
    stage["candidates"] = request_stage_candidates(
        state, config, "postcondition", messages
    )
    return {"postcondition": stage}
