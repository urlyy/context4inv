"""Request the first joint candidate set."""

from langchain_core.messages import HumanMessage, SystemMessage

from nodes.generation import request_stage_candidates
from nodes.state import WorkflowState
from prompt_templates import joint_generation_prompt, list_format_prompt


def generate_candidates(state: WorkflowState, config):
    stage = state["joint"]
    loop = state["loop"]
    format_message = SystemMessage(content=list_format_prompt)
    user_message = HumanMessage(content=joint_generation_prompt)
    stage["messages"].extend([format_message, user_message])
    messages = [
        state["program"]["formula_rules_message"],
        loop["code_message"],
        format_message,
        user_message,
    ]
    stage["candidates"] = request_stage_candidates(state, config, "joint", messages)
    stage["format_message"] = format_message
    return {"joint": stage}
