from nodes.common import (
    AgentState, StateGraph, get_experiment_switches
)
from nodes.task1.ask_llm_for_each_invariants import ask_llm_for_each_invariants
from nodes.task1.ask_llm_for_each_invariants_counterexample import ask_llm_for_each_invariants_counterexample
from nodes.task1.solve_smt_each import solve_smt_each

from common import dprint

def entry_node(state:AgentState):
    key_vars = state["loop_data"]["key_vars"]
    valid_invariants = { key_var:set() for key_var in key_vars}
    task1_data = {
        "valid_invariants": valid_invariants,
        "try_count": 0,
        "msgs": [],
    }
    return {
        "task1_data": task1_data,
    }

def finish_node(state:AgentState):
    return {}

def check_if_enabled(state: AgentState, config):
    if get_experiment_switches(config)["enable_task1"]:
        return "task1_run"
    return "task1_finish"


def check_if_retry(state:AgentState, config):
    task1_data = state["task1_data"]
    retry_limit = get_experiment_switches(config)["task1_retry_limit"]
    if task1_data['has_counterexample'] is False or task1_data["try_count"] >= retry_limit:
        return "task1_finish"
    return "ask_llm_for_each_invariants_counterexample"

def task1_add_edge(pre_node:str, g:StateGraph)->str:
    entry_name = "task1_entry"
    finish_name = "task1_finish"
    g.add_node(entry_name, entry_node)
    g.add_node(finish_name, finish_node)
    
    g.add_node("ask_llm_for_each_invariants", ask_llm_for_each_invariants)
    g.add_node("ask_llm_for_each_invariants_counterexample", ask_llm_for_each_invariants_counterexample)
    g.add_node("solve_smt_each", solve_smt_each)

    g.add_edge(pre_node, entry_name)
    g.add_conditional_edges(
        entry_name,
        check_if_enabled,
        {
            "task1_run": "ask_llm_for_each_invariants",
            "task1_finish": finish_name,
        }
    )
    g.add_edge("ask_llm_for_each_invariants", "solve_smt_each")
    g.add_edge("ask_llm_for_each_invariants_counterexample", "solve_smt_each")
    g.add_conditional_edges(
        "solve_smt_each",
        check_if_retry,
        {
            "ask_llm_for_each_invariants_counterexample": "ask_llm_for_each_invariants_counterexample",
            "task1_finish": finish_name,
        }
    )
    return finish_name