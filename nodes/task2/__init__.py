from nodes.common import (
    AgentState, StateGraph, get_experiment_switches
)
from nodes.task2.ask_llm_for_combined_invariants import ask_llm_for_combined_invariants
from nodes.task2.ask_llm_for_combined_invariants_counterexample import ask_llm_for_combined_invariants_counterexample
from nodes.task2.solve_smt_combined import solve_smt_combined

def entry_node(state:AgentState)->AgentState:
    task2_data = {
        "valid_invariants": set(),
        "try_count": 0,
        "msgs": [],
    }
    return {
        "task2_data": task2_data
    }

def finish_node(state:AgentState)->AgentState:
    return {}

def check_if_enabled(state: AgentState, config):
    if get_experiment_switches(config)["enable_task2"]:
        return "task2_run"
    return "task2_finish"


def check_if_retry(state:AgentState, config):
    task2_data = state["task2_data"]
    retry_limit = get_experiment_switches(config)["task2_retry_limit"]
    if task2_data['has_counterexample'] is False or task2_data["try_count"] >= retry_limit:
        return "task2_finish"
    return "ask_llm_for_combined_invariants_counterexample"

def task2_add_edge(pre_node:str, g:StateGraph)->str:
    entry_name = "task2_entry"
    finish_name = "task2_finish"
    g.add_node(entry_name, entry_node)
    g.add_node(finish_name, finish_node)
    
    g.add_node("ask_llm_for_combined_invariants", ask_llm_for_combined_invariants)
    g.add_node("ask_llm_for_combined_invariants_counterexample", ask_llm_for_combined_invariants_counterexample)
    g.add_node("solve_smt_combined", solve_smt_combined)

    g.add_edge(pre_node, entry_name)
    g.add_conditional_edges(
        entry_name,
        check_if_enabled,
        {
            "task2_run": "ask_llm_for_combined_invariants",
            "task2_finish": finish_name,
        }
    )
    g.add_edge("ask_llm_for_combined_invariants", "solve_smt_combined")
    g.add_edge("ask_llm_for_combined_invariants_counterexample", "solve_smt_combined")
    g.add_conditional_edges(
        "solve_smt_combined",
        check_if_retry,
        {
            "ask_llm_for_combined_invariants_counterexample": "ask_llm_for_combined_invariants_counterexample",
            "task2_finish": finish_name,
        }
    )
    return finish_name