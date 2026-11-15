"""Generate, check and refine combined loop invariants."""

from langgraph.graph import StateGraph

from nodes.config import read_experiment_options
from nodes.state import WorkflowState

from .generate_candidates import generate_candidates
from .refine_candidates import refine_candidates
from .verify_candidates import verify_candidates


def initialize_stage(state: WorkflowState):
    return {
        "combined": {
            "verified_invariants": set(),
            "generation_round": 0,
            "messages": [],
        }
    }


def finish_stage(state: WorkflowState):
    return {}


def choose_generation(state: WorkflowState, config):
    return "generate" if read_experiment_options(config).combined_enabled else "finish"


def choose_refinement(state: WorkflowState, config):
    stage = state["combined"]
    if (
        not stage["has_failures"]
        or stage["generation_round"] >= read_experiment_options(config).retry_limit
    ):
        return "finish"
    return "refine"


def build_combined_workflow(previous_node: str, graph: StateGraph) -> str:
    graph.add_node("combined_initialize", initialize_stage)
    graph.add_node("combined_generate", generate_candidates)
    graph.add_node("combined_verify", verify_candidates)
    graph.add_node("combined_refine", refine_candidates)
    graph.add_node("combined_finish", finish_stage)
    graph.add_edge(previous_node, "combined_initialize")
    graph.add_conditional_edges(
        "combined_initialize",
        choose_generation,
        {
            "generate": "combined_generate",
            "finish": "combined_finish",
        },
    )
    graph.add_edge("combined_generate", "combined_verify")
    graph.add_edge("combined_refine", "combined_verify")
    graph.add_conditional_edges(
        "combined_verify",
        choose_refinement,
        {
            "refine": "combined_refine",
            "finish": "combined_finish",
        },
    )
    return "combined_finish"
