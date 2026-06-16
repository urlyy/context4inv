from nodes.common import (
    AgentState, StateGraph
)
from nodes.func_level.next_func import next_func
from nodes.func_level.parse_func import parse_func
from nodes.func_level.find_key_vars import find_key_vars
from nodes.func_level.find_path_to_loops import find_path_to_loops
from nodes.loop_level import loop_level_add_edge

def entry_node(state:AgentState):
    func_data = {
        "loops_invs": [],
        "loops_key_vars": [],
        "loops_ssa_dicts": [],
        "loops_counterexample_vars": [],
        "gen_err": False,
    }
    state["func_data"] = func_data
    return state

def finish_node(state:AgentState):
    loops_invs = state["func_data"]["loops_invs"]
    for loop_invs in loops_invs:
        for inv in loops_invs:
            if inv == "":
                raise Exception("生成不变式失败")
    pass

def check_if_next_func(state:AgentState):
    if state["func_data"]["cur_name"] == None:
        return "func_level_finish"
    return "parse_func"

def func_level_add_edge(pre_node:str, g:StateGraph)->str:
    entry_name = "func_level_entry"
    finish_name = "func_level_finish"
    g.add_node(entry_name, entry_node)
    g.add_node(finish_name, finish_node)

    g.add_node("next_func", next_func)
    g.add_node("parse_func", parse_func)
    g.add_node("find_path_to_loops", find_path_to_loops)
    g.add_node("find_key_vars", find_key_vars)
    
    
    g.add_edge(pre_node, entry_name)
    g.add_edge(entry_name, "next_func")
    g.add_conditional_edges(
        "next_func",
        check_if_next_func,
        {
            "func_level_finish": finish_name,
            "parse_func": "parse_func",
        }
    )
    g.add_edge("parse_func", "find_key_vars")
    g.add_edge("find_key_vars", "find_path_to_loops")

    last_name = loop_level_add_edge("find_path_to_loops", g)
    g.add_edge(last_name, finish_name)
    return finish_name