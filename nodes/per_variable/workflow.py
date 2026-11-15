"""Generate, check and refine per variable loop invariants."""

from langgraph.graph import StateGraph

from nodes.config import read_experiment_options
from nodes.state import WorkflowState

from .generate_candidates import generate_candidates
from .refine_candidates import refine_candidates
from .verify_candidates import verify_candidates


def initialize_stage(state: WorkflowState):
    return {
        "per_variable": {
            "verified_invariants": {
                variable: set() for variable in state["loop"]["modified_variables"]
            },
            "generation_round": 0,
            "messages": [],
        }
    }


def finish_stage(state: WorkflowState):
    return {}


def choose_generation(state: WorkflowState, config):
    return (
        "generate" if read_experiment_options(config).per_variable_enabled else "finish"
    )


def choose_refinement(state: WorkflowState, config):
    stage = state["per_variable"]
    if (
        not stage["has_failures"]
        or stage["generation_round"] >= read_experiment_options(config).retry_limit
    ):
        return "finish"
    return "refine"


def build_per_variable_workflow(previous_node: str, graph: StateGraph) -> str:
    graph.add_node("per_variable_initialize", initialize_stage)
    graph.add_node("per_variable_generate", generate_candidates)
    graph.add_node("per_variable_verify", verify_candidates)
    graph.add_node("per_variable_refine", refine_candidates)
    graph.add_node("per_variable_finish", finish_stage)
    graph.add_edge(previous_node, "per_variable_initialize")
    graph.add_conditional_edges(
        "per_variable_initialize",
        choose_generation,
        {
            "generate": "per_variable_generate",
            "finish": "per_variable_finish",
        },
    )
    graph.add_edge("per_variable_generate", "per_variable_verify")
    graph.add_edge("per_variable_refine", "per_variable_verify")
    graph.add_conditional_edges(
        "per_variable_verify",
        choose_refinement,
        {
            "refine": "per_variable_refine",
            "finish": "per_variable_finish",
        },
    )
    return "per_variable_finish"
