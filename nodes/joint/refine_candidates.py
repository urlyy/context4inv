from langchain_core.messages import HumanMessage

from nodes.feedback import format_generation_rejections
from nodes.generation import request_stage_candidates
from nodes.state import WorkflowState
from prompt_templates import joint_refinement_prompt


def refine_candidates(state: WorkflowState, config):
    stage = state["joint"]
    loop = state["loop"]
    content = format_generation_rejections(
        stage["rejections"],
        loop["counterexample_variables"],
        loop["ssa_states"],
    )
    user_message = HumanMessage(content=joint_refinement_prompt.format(content=content))
    stage["messages"].append(user_message)
    messages = [
        state["program"]["formula_rules_message"],
        loop["code_message"],
        stage["format_message"],
        user_message,
    ]
    stage["candidates"] = request_stage_candidates(
        state,
        config,
        "joint",
        messages,
    )
    return {"joint": stage}
