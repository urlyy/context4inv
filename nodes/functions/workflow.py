"""Process each defined function and collect its verified loop invariants."""

from langgraph.graph import StateGraph

from nodes.functions.key_variables import find_loop_variables
from nodes.functions.loop_paths import find_loop_paths
from nodes.functions.next_function import next_function
from nodes.functions.parser import parse_function
from nodes.loops import build_loop_workflow
from nodes.state import WorkflowState


def finish_function(state: WorkflowState):
    function = state["function"]
    program = state["program"]
    program["function_invariants"][function["name"]] = [
        set(invariants) for invariants in function["loop_invariants"]
    ]
    return {"program": program}


def route_function(state: WorkflowState):
    if state["function"]["name"] is None:
        return "functions_finished"
    return "parse_function"


def build_function_workflow(previous_node: str, graph: StateGraph) -> str:
    graph.add_node("functions_finished", lambda state: {})
    graph.add_node("next_function", next_function)
    graph.add_node("parse_function", parse_function)
    graph.add_node("find_loop_variables", find_loop_variables)
    graph.add_node("find_loop_paths", find_loop_paths)
    graph.add_node("finish_function", finish_function)

    graph.add_edge(previous_node, "next_function")
    graph.add_conditional_edges(
        "next_function",
        route_function,
        {
            "functions_finished": "functions_finished",
            "parse_function": "parse_function",
        },
    )
    graph.add_edge("parse_function", "find_loop_variables")
    graph.add_edge("find_loop_variables", "find_loop_paths")
    loops_finished = build_loop_workflow("find_loop_paths", graph)
    graph.add_edge(loops_finished, "finish_function")
    graph.add_edge("finish_function", "next_function")
    return "functions_finished"
