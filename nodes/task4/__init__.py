from nodes.common import (
    AgentState, StateGraph,get_loop_subject_dir, get_experiment_switches
)
from nodes.task4.ask_llm_for_invariants_counterexample import ask_llm_for_invariants_counterexample
from nodes.task4.solve_smt import solve_smt

from prompt_templates import task4_format_prompt
from langchain_core.messages import SystemMessage

import os

def write_logs(config, func_name, loop_id, loops_invs, msgs):
    subject_dir = get_loop_subject_dir(config,func_name, loop_id)
    # 写入消息
    log_file = os.path.join(subject_dir, "run_task4.log")
    with open(log_file, "w") as f:
        f.write("\n".join([msg.pretty_repr() for msg in msgs]))
        for loop_id, invs in enumerate(loops_invs):
            f.write(f"\n- LOOP_{loop_id} INVARIANTS: {list(invs)}")


# 如果task3失败，到这里
# 直接问个大的，让他自由增
# 问三回，不行就不行
def entry_node(state:AgentState)->AgentState:
    task3_data = state["task3_data"]
    loop_data = state["loop_data"]
    loop_id = loop_data["cur_id"]
    counterexample = task3_data["counterexample"]
    ce_and_loop_id = (counterexample, loop_id)

    func_data = state["func_data"]
    func_data["loops_invs"].append(task3_data["valid_invariants"])
    task4_data = {
        "format_msg": SystemMessage(content=task4_format_prompt),
        "has_counterexample": False,
        "ce_and_loop_id": ce_and_loop_id,
        # "llm_gen": set(),
        # "counterexample": None,
        # "valid_invariants": set(),
        "try_count": 0,
        "msgs": [],
    }
    return {
        "task4_data": task4_data,
        "func_data": func_data,
    }

def finish_node(state:AgentState)->AgentState:
    return {}

def check_if_retry(state:AgentState, config):
    retry_limit = get_experiment_switches(config)["task4_retry_limit"]
    task4_data = state["task4_data"]
    func_data = state["func_data"]
    loop_data = state["loop_data"]
    if task4_data['has_counterexample'] is False:
        write_logs(config, func_data["cur_name"], loop_data["cur_id"], func_data["loops_invs"], task4_data["msgs"])
        return "task4_finish"
    if task4_data["try_count"] >= retry_limit:
        write_logs(config, func_data["cur_name"], loop_data["cur_id"], func_data["loops_invs"], task4_data["msgs"])
        func_name = state["func_data"]["cur_name"]
        loop_id = state["loop_data"]["cur_id"]
        raise Exception(f"{func_name}-LOOP_{loop_id}生成不变式失败")
    return "ask_llm_for_invariants_counterexample"

def check_if_continue(state:AgentState, config):
    loop_data = state["loop_data"]
    loop_id = loop_data["cur_id"]
    func_name = state["func_data"]["cur_name"]
    if loop_id == 0:
        raise Exception(f"{func_name}-LOOP_{loop_id}生成不变式失败")
        # return "task4_finish"
    return "task4_entry"

def task4_add_edge(pre_node:str, g:StateGraph)->str:
    entry_name = "task4_entry"
    finish_name = "task4_finish"
    g.add_node(entry_name, entry_node)
    g.add_node(finish_name, finish_node)
    
    g.add_node("ask_llm_for_invariants_counterexample", ask_llm_for_invariants_counterexample)
    g.add_node("solve_smt", solve_smt)

    g.add_conditional_edges(
        pre_node,
        check_if_continue,
        {
            "task4_finish": finish_name,
            "task4_entry": entry_name,
        }
    )
    g.add_edge(entry_name, "ask_llm_for_invariants_counterexample")
    g.add_edge("ask_llm_for_invariants_counterexample", "solve_smt")
    g.add_conditional_edges(
        "solve_smt",
        check_if_retry,
        {
            "ask_llm_for_invariants_counterexample": "ask_llm_for_invariants_counterexample",
            "task4_finish": finish_name,
        }
    )
    return finish_name