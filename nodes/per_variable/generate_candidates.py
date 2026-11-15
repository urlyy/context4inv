"""Request the first per variable candidate set."""

from langchain_core.messages import HumanMessage, SystemMessage

from nodes.generation import request_stage_candidates
from nodes.state import WorkflowState
from prompt_templates import per_variable_format_prompt, per_variable_generation_prompt


def generate_candidates(state: WorkflowState, config):
    stage = state["per_variable"]
    loop = state["loop"]
    format_message = SystemMessage(content=per_variable_format_prompt)
    user_message = HumanMessage(content=per_variable_generation_prompt)
    stage["messages"].extend([format_message, user_message])
    messages = [
        state["program"]["formula_rules_message"],
        loop["code_message"],
        format_message,
        user_message,
    ]
    stage["candidates"] = request_stage_candidates(
        state,
        config,
        "per_variable",
        messages,
        grouped=True,
        allowed_keys=loop["modified_variables"],
    )
    stage["format_message"] = format_message
    return {"per_variable": stage}
