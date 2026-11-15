"""Start program analysis before processing functions in dependency order."""

from langgraph.graph import StateGraph

from nodes.functions import build_function_workflow
from nodes.program.call_graph import analyze_program


def build_program_workflow(previous_node: str, graph: StateGraph) -> str:
    graph.add_node("analyze_program", analyze_program)
    graph.add_edge(previous_node, "analyze_program")
    return build_function_workflow("analyze_program", graph)
