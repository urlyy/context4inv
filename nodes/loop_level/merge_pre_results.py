import json
from nodes.common import AgentState, get_experiment_switches, get_loop_subject_dir
from common import dprint
import os

def merge_pre_results(state: AgentState, config) -> AgentState:
    func_data = state["func_data"]
    loop_data = state["loop_data"]
    task1_data = state["task1_data"]
    task2_data = state["task2_data"]
    task12_data = state["task12_data"]
    switches = get_experiment_switches(config)
    task1_res = task1_data["valid_invariants"]
    task2_res = task2_data["valid_invariants"]
    task12_res = task12_data["valid_invariants"]
    loop_invs = list()

    dprint(f"inv_each:     {task1_res}")
    dprint(f"inv_combined: {task2_res}")
    dprint(f"inv_task12:   {task12_res}")

    if switches["enable_task12"]:
        for inv in task12_res:
            if inv not in loop_invs:
                loop_invs.append(inv)
    else:
        for invs in task1_res.values():
            for inv in invs:
                if inv not in loop_invs:
                    loop_invs.append(inv)
        for inv in task2_res:
            if inv not in loop_invs:
                loop_invs.append(inv)

    if len(loop_invs) == 0:
        raise Exception("前置任务无正确不变式生成")

    subject_dir = get_loop_subject_dir(config,func_data["cur_name"], loop_data["cur_id"])
    if switches["enable_task12"]:
        task12_log_file = os.path.join(subject_dir, "run_task12.log")
        with open(task12_log_file, "w") as f:
            f.write("\n".join([msg.pretty_repr() for msg in task12_data["msgs"]]))
    else:
        each_log_file = os.path.join(subject_dir, "run_each.log")
        with open(each_log_file, "w") as f:
            f.write("\n".join([msg.pretty_repr() for msg in task1_data["msgs"]]))
        combined_log_file = os.path.join(subject_dir, "run_combined.log")
        with open(combined_log_file, "w") as f:
            f.write("\n".join([msg.pretty_repr() for msg in task2_data["msgs"]]))

    inv_file = os.path.join(subject_dir, "invariants_pre.json")
    json.dump(loop_invs, open(inv_file, "w"))

    task3_data = {
        "valid_invariants": set(loop_invs)
    }

    return {
        "task3_data": task3_data
    }