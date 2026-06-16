from nodes.common import (
    AgentState, LoopNode, StateGraph, get_loop_subject_dir
)
from nodes.loop_level.next_loop import next_loop
from nodes.loop_level.generate_z3_template import generate_z3_template
from nodes.loop_level.merge_pre_results import merge_pre_results

from nodes.task1 import task1_add_edge
from nodes.task2 import task2_add_edge
from nodes.task12 import task12_add_edge
from nodes.task3 import task3_add_edge

def finish_node(state:AgentState, config):
    return {}

def entry_node(state:AgentState):
    loop_data = {
        "cur_id": -1,
    }
    state["loop_data"] = loop_data
    return state

def check_if_retry_task1_2(state:AgentState):
    pass

def check_if_next_loop(state:AgentState):
    if state["loop_data"]["cur_id"] == len(state["func_data"]["path_to_loops"]):
        return "loop_level_finish"
    return "generate_z3_template"

def check_if_task2(state:AgentState):
    loop_data = state["loop_data"]
    loop_ir_node:LoopNode = loop_data["path_to_loop"][-1]
    if loop_ir_node.post_condition is None:
        return "task2_start"
    pass

def loop_level_add_edge(pre_node:str, g:StateGraph)->str:
    finish_name = "loop_level_finish"
    entry_name = "loop_level_entry"
    g.add_node(entry_name, entry_node)
    g.add_node(finish_name, finish_node)
    
    g.add_node("next_loop", next_loop)
    g.add_node("generate_z3_template", generate_z3_template)
    g.add_node("merge_pre_results", merge_pre_results)
    
    # g.add_node("find_path_to_loops", find_path_to_loops)
    
    g.add_edge(pre_node, entry_name)
    g.add_edge(entry_name, "next_loop")
    g.add_conditional_edges(
        "next_loop",
        check_if_next_loop,
        {
            "loop_level_finish": "loop_level_finish",
            "generate_z3_template": "generate_z3_template",
        }
    )
    # g.add_edge("generate_z3_template", finish_name)
    end_task1 = task1_add_edge("generate_z3_template", g)
    end_task2 = task2_add_edge("generate_z3_template", g)
    end_task12 = task12_add_edge("generate_z3_template", g)
    g.add_edge([end_task1, end_task2, end_task12], "merge_pre_results")
    end_task3 = task3_add_edge("merge_pre_results", g)
    g.add_edge(end_task3, "next_loop")
    return finish_name