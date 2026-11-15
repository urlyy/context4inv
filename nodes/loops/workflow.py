"""Generate loop candidates, merge valid results, then verify the postcondition."""

from langgraph.graph import StateGraph

from nodes.combined import build_combined_workflow
from nodes.joint import build_joint_workflow
from nodes.loops.merge_invariants import merge_invariants
from nodes.loops.next_loop import next_loop
from nodes.loops.verification_templates import prepare_verification_templates
from nodes.per_variable import build_per_variable_workflow
from nodes.postcondition import build_postcondition_workflow
from nodes.state import WorkflowState


def initialize_loops(state: WorkflowState):
    return {"loop": {"index": -1}}


def route_loop(state: WorkflowState):
    if state["loop"]["index"] == len(state["function"]["loop_paths"]):
        return "loops_finished"
    return "prepare_verification_templates"


def build_loop_workflow(previous_node: str, graph: StateGraph) -> str:
    graph.add_node("initialize_loops", initialize_loops)
    graph.add_node("loops_finished", lambda state: {})
    graph.add_node("next_loop", next_loop)
    graph.add_node("prepare_verification_templates", prepare_verification_templates)
    graph.add_node("merge_invariants", merge_invariants)
    graph.add_edge(previous_node, "initialize_loops")
    graph.add_edge("initialize_loops", "next_loop")
    graph.add_conditional_edges(
        "next_loop",
        route_loop,
        {
            "loops_finished": "loops_finished",
            "prepare_verification_templates": "prepare_verification_templates",
        },
    )
    candidate_stages = [
        build("prepare_verification_templates", graph)
        for build in (
            build_per_variable_workflow,
            build_combined_workflow,
            build_joint_workflow,
        )
    ]
    graph.add_edge(candidate_stages, "merge_invariants")
    postcondition_finished = build_postcondition_workflow("merge_invariants", graph)
    graph.add_edge(postcondition_finished, "next_loop")
    return "loops_finished"
