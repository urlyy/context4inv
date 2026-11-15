"""Generate, check and refine joint loop invariants."""

from langgraph.graph import StateGraph

from nodes.config import read_experiment_options
from nodes.state import WorkflowState

from .generate_candidates import generate_candidates
from .refine_candidates import refine_candidates
from .verify_candidates import verify_candidates


def initialize_stage(state: WorkflowState):
    return {
        "joint": {
            "verified_invariants": set(),
            "generation_round": 0,
            "messages": [],
        }
    }


def finish_stage(state: WorkflowState):
    return {}


def choose_generation(state: WorkflowState, config):
    return "generate" if read_experiment_options(config).joint_enabled else "finish"


def choose_refinement(state: WorkflowState, config):
    stage = state["joint"]
    if (
        not stage["has_failures"]
        or stage["generation_round"] >= read_experiment_options(config).retry_limit
    ):
        return "finish"
    return "refine"


def build_joint_workflow(previous_node: str, graph: StateGraph) -> str:
    graph.add_node("joint_initialize", initialize_stage)
    graph.add_node("joint_generate", generate_candidates)
    graph.add_node("joint_verify", verify_candidates)
    graph.add_node("joint_refine", refine_candidates)
    graph.add_node("joint_finish", finish_stage)
    graph.add_edge(previous_node, "joint_initialize")
    graph.add_conditional_edges(
        "joint_initialize",
        choose_generation,
        {
            "generate": "joint_generate",
            "finish": "joint_finish",
        },
    )
    graph.add_edge("joint_generate", "joint_verify")
    graph.add_edge("joint_refine", "joint_verify")
    graph.add_conditional_edges(
        "joint_verify",
        choose_refinement,
        {
            "refine": "joint_refine",
            "finish": "joint_finish",
        },
    )
    return "joint_finish"
