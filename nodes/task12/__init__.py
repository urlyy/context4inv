from nodes.common import (
    AgentState, StateGraph, get_experiment_switches
)
from nodes.task12.ask_llm_for_invariants import ask_llm_for_invariants
from nodes.task12.ask_llm_for_invariants_counterexample import ask_llm_for_invariants_counterexample
from nodes.task12.solve_smt import solve_smt


def entry_node(state: AgentState) -> AgentState:
    task12_data = {
        "valid_invariants": set(),
        "try_count": 0,
        "msgs": [],
    }
    return {
        "task12_data": task12_data,
    }


def finish_node(state: AgentState) -> AgentState:
    return {}


def check_if_enabled(state: AgentState, config):
    if get_experiment_switches(config)["enable_task12"]:
        return "task12_run"
    return "task12_finish"


def check_if_retry(state: AgentState, config):
    task12_data = state["task12_data"]
    retry_limit = get_experiment_switches(config)["task12_retry_limit"]
    if task12_data["has_counterexample"] is False or task12_data["try_count"] >= retry_limit:
        return "task12_finish"
    return "ask_llm_for_invariants_counterexample"


def task12_add_edge(pre_node: str, g: StateGraph) -> str:
    entry_name = "task12_entry"
    finish_name = "task12_finish"
    g.add_node(entry_name, entry_node)
    g.add_node(finish_name, finish_node)

    g.add_node("ask_llm_for_task12_invariants", ask_llm_for_invariants)
    g.add_node("ask_llm_for_task12_invariants_counterexample", ask_llm_for_invariants_counterexample)
    g.add_node("solve_smt_task12", solve_smt)

    g.add_edge(pre_node, entry_name)
    g.add_conditional_edges(
        entry_name,
        check_if_enabled,
        {
            "task12_run": "ask_llm_for_task12_invariants",
            "task12_finish": finish_name,
        }
    )
    g.add_edge("ask_llm_for_task12_invariants", "solve_smt_task12")
    g.add_edge("ask_llm_for_task12_invariants_counterexample", "solve_smt_task12")
    g.add_conditional_edges(
        "solve_smt_task12",
        check_if_retry,
        {
            "ask_llm_for_invariants_counterexample": "ask_llm_for_task12_invariants_counterexample",
            "task12_finish": finish_name,
        }
    )
    return finish_name
