"""Check the target assertion, refine its invariant, or strengthen earlier loops."""

import json

from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph

from nodes.artifacts import loop_directory
from nodes.config import read_experiment_options
from nodes.state import WorkflowState
from nodes.strengthening import build_strengthening_workflow
from prompt_templates import list_format_prompt

from .refine_candidates import refine_candidates
from .verify_candidates import verify_candidates
from .verify_postcondition import verify_postcondition


def write_postcondition_artifacts(state: WorkflowState, config):
    function = state["function"]
    stage = state["postcondition"]
    folder = loop_directory(config, function["name"], state["loop"]["index"])
    (folder / "run_postcondition.log").write_text(
        "\n".join(message.pretty_repr() for message in stage.get("messages", ())),
        encoding="utf-8",
    )
    (folder / "invariants_post.json").write_text(
        json.dumps(sorted(stage["verified_invariants"])),
        encoding="utf-8",
    )


def save_loop_invariants(state: WorkflowState, config):
    function = state["function"]
    loop_index = state["loop"]["index"]
    invariants = set(state["postcondition"]["verified_invariants"])
    if loop_index == len(function["loop_invariants"]):
        function["loop_invariants"].append(invariants)
    else:
        function["loop_invariants"][loop_index] = invariants
    write_postcondition_artifacts(state, config)
    return {"function": function}


def initialize_stage(state: WorkflowState):
    stage = state["postcondition"]
    # The first assertion check uses the candidates already generated upstream.
    # Its zero round precedes the first model refinement, preserving its budget.
    stage.update(
        generation_round=-1,
        format_message=SystemMessage(content=list_format_prompt),
        messages=[],
    )
    return {"postcondition": stage}


def choose_assertion_check(state: WorkflowState):
    return "finish" if state["loop"]["path"][-1].postcondition is None else "check"


def choose_next_step(state: WorkflowState, config):
    stage = state["postcondition"]
    options = read_experiment_options(config)
    if not stage["has_failures"]:
        write_postcondition_artifacts(state, config)
        return "finish"
    if stage["generation_round"] < options.retry_limit:
        return "refine"
    write_postcondition_artifacts(state, config)
    if not options.strengthening_enabled:
        raise RuntimeError(
            f"{state['function']['name']}-LOOP_{state['loop']['index']}: assertion not proved; earlier-loop strengthening is disabled"
        )
    return "strengthen"


def request_strengthening(state: WorkflowState):
    return {}


def build_postcondition_workflow(previous_node: str, graph: StateGraph) -> str:
    graph.add_node("postcondition_initialize", initialize_stage)
    graph.add_node("postcondition_check", verify_postcondition)
    graph.add_node("postcondition_refine", refine_candidates)
    graph.add_node("postcondition_verify_candidates", verify_candidates)
    graph.add_node("postcondition_request_strengthening", request_strengthening)
    graph.add_node("postcondition_finish", save_loop_invariants)
    graph.add_conditional_edges(
        previous_node,
        choose_assertion_check,
        {
            "check": "postcondition_initialize",
            "finish": "postcondition_finish",
        },
    )
    graph.add_edge("postcondition_initialize", "postcondition_check")
    graph.add_conditional_edges(
        "postcondition_check",
        choose_next_step,
        {
            "finish": "postcondition_finish",
            "refine": "postcondition_refine",
            "strengthen": "postcondition_request_strengthening",
        },
    )
    graph.add_edge("postcondition_refine", "postcondition_verify_candidates")
    graph.add_edge("postcondition_verify_candidates", "postcondition_check")
    strengthening_finish = build_strengthening_workflow(
        "postcondition_request_strengthening", graph
    )
    graph.add_edge(strengthening_finish, "postcondition_finish")
    return "postcondition_finish"
