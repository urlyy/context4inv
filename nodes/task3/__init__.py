import json
from nodes.common import (
    AgentState, LoopNode, StateGraph
)
from langchain_core.messages import SystemMessage
from nodes.task3.ask_llm_for_invariants_counterexample_post import ask_llm_for_invariants_counterexample_post
from nodes.task3.solve_smt_post_single import solve_smt_post_single
from nodes.task3.solve_smt_post_conjuct import solve_smt_post_conjuct

from nodes.task4 import task4_add_edge

import os

from nodes.common import AgentState, get_loop_subject_dir
from nodes.common import get_experiment_switches

# 和2共用
from prompt_templates import task2_format_prompt

def write_logs(config, func_name, loop_id, invariants, msgs):
    subject_dir = get_loop_subject_dir(config,func_name, loop_id)
    # 写入消息
    post_log_file = os.path.join(subject_dir, "run_post.log")
    with open(post_log_file, "w") as f:
        f.write("\n".join([msg.pretty_repr() for msg in msgs]))
    # 写入不变式
    inv_file = os.path.join(subject_dir, "invariants_post.json")
    json.dump(invariants, open(inv_file, "w"))

def finish_node(state:AgentState)->AgentState:
    func_data = state["func_data"]
    valid_invs = state["task3_data"]["valid_invariants"]
    func_data["loops_invs"].append(valid_invs)
    return {
        "func_data": func_data,
    }

def entry_node(state:AgentState)->AgentState:
    task3_data = state["task3_data"]
    task3_data["try_count"]=-1
    task3_data["format_msg"] = SystemMessage(content=task2_format_prompt)
    task3_data["msgs"] = []
    return {
        "task3_data": task3_data,
    }

def check_where_to_go(state:AgentState, config):
    switches = get_experiment_switches(config)
    task3_data = state["task3_data"]
    func_data = state["func_data"]
    loop_data = state["loop_data"]
    final_invariants = list(task3_data["valid_invariants"])
    if task3_data['has_counterexample'] is False:
        write_logs(config, func_data["cur_name"], loop_data["cur_id"], final_invariants, task3_data["msgs"])
        return "task3_finish"
    # 回溯
    if task3_data["try_count"] >= switches["task3_retry_limit"]:
        # print("要回溯")
        write_logs(config, func_data["cur_name"], loop_data["cur_id"], final_invariants, task3_data["msgs"])
        if not switches["enable_task4_pre_enhance"]:
            func_name = func_data["cur_name"]
            loop_id = loop_data["cur_id"]
            raise Exception(
                f"{func_name}-LOOP_{loop_id}后置不变式失败，且实验开关已关闭task4前置循环增强"
            )
        # for msg in task3_data["msgs"]:
        #     msg.pretty_print()
        # raise Exception("失败")
        return "to_task4"
    return "ask_llm_for_invariants_counterexample_post"

def check_if_continue(state:AgentState):
    loop_data = state["loop_data"]
    loop_ir_node:LoopNode = loop_data["path_to_loop"][-1]
    if loop_ir_node.post_condition is None:
        return "task3_finish"
    return "task3_entry"

def to_task4(state:AgentState):
    pass

def task3_add_edge(pre_node:str, g:StateGraph)->str:
    entry_name = "task3_entry"
    finish_name = "task3_finish"
    
    g.add_node(entry_name, entry_node)
    g.add_node(finish_name, finish_node)
    
    g.add_node("solve_smt_post_conjuct", solve_smt_post_conjuct)
    g.add_node("ask_llm_for_invariants_counterexample_post", ask_llm_for_invariants_counterexample_post)
    g.add_node("solve_smt_post_single", solve_smt_post_single)
    g.add_node("to_task4", to_task4)

    g.add_conditional_edges(
        pre_node,
        check_if_continue,
        {
            "task3_finish": finish_name,
            "task3_entry": entry_name,
        }
    )
    g.add_edge(entry_name, "solve_smt_post_conjuct")
    g.add_conditional_edges(
        "solve_smt_post_conjuct",
        check_where_to_go,
        {
            "ask_llm_for_invariants_counterexample_post": "ask_llm_for_invariants_counterexample_post",
            "task3_finish": finish_name,
            "to_task4": "to_task4",
        }
    )
    g.add_edge("ask_llm_for_invariants_counterexample_post", "solve_smt_post_single")
    g.add_edge("solve_smt_post_single", "solve_smt_post_conjuct")

    end_task4 = task4_add_edge("to_task4",g)
    g.add_edge(end_task4, finish_name)
    return finish_name