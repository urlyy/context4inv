"""Request additions with both assertion and rejected-candidate diagnostics."""

from langchain_core.messages import HumanMessage, SystemMessage

from nodes.feedback import format_candidate_rejections, format_solver_diagnostic
from nodes.formulas import conjoin_invariants
from nodes.generation import request_stage_candidates
from nodes.source_rendering import render_function_source
from nodes.state import WorkflowState
from prompt_templates import strengthening_code_prompt, strengthening_refinement_prompt


def _loop_descriptions(function):
    descriptions = []
    for loop_index, invariants in enumerate(function["loop_invariants"]):
        detail = {
            "key_variables": function["modified_variables_by_loop"][loop_index],
            "invariants": sorted(invariants),
        }
        descriptions.append(f"- LOOP_{loop_index}: {detail}")
    return "\n".join(descriptions)


def _failure_diagnostics(state):
    function = state["function"]
    stage = state["strengthening"]
    location = stage["failure_location"]
    loop_index = location.loop_index
    diagnostic = format_solver_diagnostic(
        conjoin_invariants(function["loop_invariants"][loop_index]),
        location.failure,
        function["counterexample_variables_by_loop"][loop_index],
        function["ssa_states_by_loop"][loop_index],
    )
    for loop_index in range(state["loop"]["index"] + 1):
        diagnostic += "\n" + format_candidate_rejections(
            stage.get("rejections_by_loop", {}).get(loop_index, {}).values(),
            stage.get("invalid_candidates_by_loop", {}).get(loop_index, ()),
            f"LOOP_{loop_index}",
            function["counterexample_variables_by_loop"][loop_index],
            function["ssa_states_by_loop"][loop_index],
        )
    return diagnostic


def refine_candidates(state: WorkflowState, config):
    function = state["function"]
    stage = state["strengthening"]
    location = stage["failure_location"]
    code_message = SystemMessage(
        content=strengthening_code_prompt.format(
            func_code=render_function_source(function, include_invariants=False),
            loop_detail=_loop_descriptions(function),
        )
    )
    user_message = HumanMessage(
        content=strengthening_refinement_prompt.format(
            ce_loop_name=f"LOOP_{location.loop_index}",
            ce_prompt=_failure_diagnostics(state),
            target_loop_name=f"LOOP_{state['loop']['index']}",
        )
    )
    stage["messages"].extend([code_message, user_message])
    messages = [
        state["program"]["formula_rules_message"],
        code_message,
        user_message,
        stage["format_message"],
    ]
    candidates = request_stage_candidates(
        state,
        config,
        "strengthening",
        messages,
        grouped=True,
        loop_count=state["loop"]["index"] + 1,
    )
    stage["candidates"] = candidates
    stage["first_modified_loop"] = min(
        int(name.removeprefix("LOOP_")) for name in candidates
    )
    stage["generation_round"] += 1
    return {"strengthening": stage}
