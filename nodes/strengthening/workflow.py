"""Strengthen earlier loop summaries and recheck every affected loop."""

from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph

from nodes.artifacts import loop_directory
from nodes.config import read_experiment_options
from nodes.state import LoopFailure, WorkflowState
from prompt_templates import strengthening_format_prompt

from .refine_candidates import refine_candidates
from .verify_candidates import verify_candidates


def write_strengthening_log(state: WorkflowState, config):
    function = state["function"]
    stage = state["strengthening"]
    lines = [message.pretty_repr() for message in stage["messages"]]
    lines.extend(
        f"- LOOP_{index} INVARIANTS: {sorted(invariants)}"
        for index, invariants in enumerate(function["loop_invariants"])
    )
    folder = loop_directory(config, function["name"], state["loop"]["index"])
    (folder / "run_strengthening.log").write_text("\n".join(lines), encoding="utf-8")


def initialize_stage(state: WorkflowState):
    postcondition = state["postcondition"]
    loop_index = state["loop"]["index"]
    state["function"]["loop_invariants"].append(
        set(postcondition["verified_invariants"])
    )
    return {
        "function": state["function"],
        "strengthening": {
            "format_message": SystemMessage(content=strengthening_format_prompt),
            "has_failures": False,
            "failure_location": LoopFailure(loop_index, postcondition["failure"]),
            "generation_round": 0,
            "messages": [],
            "rejections_by_loop": {
                loop_index: dict(postcondition.get("candidate_rejections", {}))
            },
            "invalid_candidates_by_loop": {
                loop_index: list(postcondition.get("invalid_candidates", ()))
            },
        },
    }


def finish_strengthening(state: WorkflowState):
    postcondition = state["postcondition"]
    postcondition["verified_invariants"] = set(
        state["function"]["loop_invariants"][state["loop"]["index"]]
    )
    postcondition["has_failures"] = False
    return {"postcondition": postcondition}


def choose_initialization(state: WorkflowState):
    if state["loop"]["index"] == 0:
        raise RuntimeError(
            f"{state['function']['name']}-LOOP_0: no earlier loop can be strengthened"
        )
    return "initialize"


def choose_next_step(state: WorkflowState, config):
    stage = state["strengthening"]
    if not stage["has_failures"]:
        write_strengthening_log(state, config)
        return "finish"
    if stage["generation_round"] >= read_experiment_options(config).retry_limit:
        write_strengthening_log(state, config)
        raise RuntimeError(
            f"{state['function']['name']}-LOOP_{state['loop']['index']}: invariant strengthening exhausted its generation budget"
        )
    return "refine"


def build_strengthening_workflow(previous_node: str, graph: StateGraph) -> str:
    graph.add_node("strengthening_initialize", initialize_stage)
    graph.add_node("strengthening_refine", refine_candidates)
    graph.add_node("strengthening_verify", verify_candidates)
    graph.add_node("strengthening_finish", finish_strengthening)
    graph.add_conditional_edges(
        previous_node, choose_initialization, {"initialize": "strengthening_initialize"}
    )
    graph.add_edge("strengthening_initialize", "strengthening_refine")
    graph.add_edge("strengthening_refine", "strengthening_verify")
    graph.add_conditional_edges(
        "strengthening_verify",
        choose_next_step,
        {
            "refine": "strengthening_refine",
            "finish": "strengthening_finish",
        },
    )
    return "strengthening_finish"
