from nodes.common import (
    AgentState, StateGraph
)
from nodes.global_level.gen_inverted_call_graph import gen_inverted_call_graph
from nodes.func_level import func_level_add_edge

def add_edge(pre_node:str, g:StateGraph)->str:
    g.add_node("gen_inverted_call_graph", gen_inverted_call_graph)

    g.add_edge(pre_node, "gen_inverted_call_graph")
    last_node = func_level_add_edge("gen_inverted_call_graph", g)
    return last_node