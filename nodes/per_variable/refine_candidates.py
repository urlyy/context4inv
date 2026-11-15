from langchain_core.messages import HumanMessage

from nodes.feedback import format_generation_rejections
from nodes.generation import request_stage_candidates
from nodes.state import WorkflowState
from prompt_templates import per_variable_refinement_prompt


def refine_candidates(state: WorkflowState, config):
    stage = state["per_variable"]
    loop = state["loop"]
    sections = []
    for variable, rejections in stage["rejections"].items():
        sections.append(
            f"Wrong loop invariants of the variable `{variable}`:\n"
            + format_generation_rejections(
                rejections,
                loop["counterexample_variables"],
                loop["ssa_states"],
            )
        )
    content = "\n".join(sections)
    user_message = HumanMessage(
        content=per_variable_refinement_prompt.format(content=content)
    )
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
        "per_variable",
        messages,
        grouped=True,
        allowed_keys=loop["modified_variables"],
    )
    return {"per_variable": stage}
