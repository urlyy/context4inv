import json
import os
import traceback
from langchain_core.messages import ToolMessage

from nodes.common import (
    AgentState,
    LoopNode,
    conjuct_invariants,
    get_err_log_path,
    get_experiment_switches,
    get_pre_task_z3_template_path,
    get_verify_dir,
    trans_invariant,
)
from utils.fol_parser import replace_old_for_solve
from utils.solve_smt import solve_smt as _solve_smt


def __solve(config, invariant: str, func_name, loop_id, key_vars, ssa_dict, idx: int, new_try_count: int, valid_invariants: set[str]):
    verify_dir = get_verify_dir(config, func_name, loop_id)
    template_file_path = get_pre_task_z3_template_path(config, func_name, loop_id)
    err_log_path = get_err_log_path(config, func_name, loop_id)
    try:
        new_invs = [invariant] + list(valid_invariants)
        new_inv = conjuct_invariants(new_invs)
        inv_replaced_old = replace_old_for_solve(new_inv, key_vars)
        quantifier_binder_var_init_code, final_invariant, z3_invariant = trans_invariant(inv_replaced_old, key_vars, ssa_dict)
    except Exception:
        with open(err_log_path, "a") as f:
            f.write("When solve_task12 parsing:\n")
            traceback.print_exc(file=f)
            f.write("\n\n")
        return False, None, None

    with open(template_file_path, "r") as f:
        solve_template = f.read()
    filled_solve_code = solve_template.format(quantifier_binder_var_init_code, invariant, z3_invariant)

    prefix = f"pre-task12-try_{new_try_count}-idx_{idx}"
    filled_solve_file = os.path.join(verify_dir, f"{prefix}.py")
    with open(filled_solve_file, "w") as f:
        f.write(filled_solve_code)
    try:
        valid, data, duration = _solve_smt(filled_solve_file)
    except Exception as e:
        with open(err_log_path, "a") as f:
            f.write(f"{e}\nWhen solve_task12 solving.\n\n")
        return False, None, None
    return True, valid, data


def solve_smt(state: AgentState, config) -> AgentState:
    task12_data = state["task12_data"]
    loop_data = state["loop_data"]
    func_data = state["func_data"]

    func_name = func_data["cur_name"]
    path_to_loop = loop_data["path_to_loop"]
    key_vars = loop_data["key_vars"]
    ssa_dict = loop_data["ssa_dict_before_loop"]
    llm_gen = task12_data["llm_gen"]
    valid_invariants = task12_data["valid_invariants"]
    msgs = task12_data["msgs"]

    loop_ir_node: LoopNode = path_to_loop[-1]
    new_try_count = task12_data["try_count"] + 1
    iterative = get_experiment_switches(config)["enable_iterative"]

    has_counterexample = False
    invalid_invariants_and_reason = []
    idx = -1

    if iterative:
        while True:
            new_invariants_found = False
            current_candidates = list(llm_gen)
            for inv in current_candidates:
                if inv in valid_invariants:
                    continue
                idx += 1
                no_err, valid, data = __solve(
                    config,
                    inv,
                    func_name,
                    loop_ir_node.loop_id,
                    key_vars,
                    ssa_dict,
                    idx,
                    new_try_count,
                    valid_invariants,
                )
                if not no_err:
                    llm_gen.remove(inv)
                    continue
                if not valid:
                    if isinstance(data, tuple):
                        invalid_invariants_and_reason.append((inv, data[0], data[1], data[2]))
                        has_counterexample = True
                else:
                    valid_invariants.add(inv)
                    new_invariants_found = True
            if not new_invariants_found:
                break
    else:
        for inv in list(llm_gen):
            if inv in valid_invariants:
                continue
            idx += 1
            no_err, valid, data = __solve(
                config,
                inv,
                func_name,
                loop_ir_node.loop_id,
                key_vars,
                ssa_dict,
                idx,
                new_try_count,
                valid_invariants,
            )
            if not no_err:
                llm_gen.remove(inv)
                continue
            if not valid:
                if isinstance(data, tuple):
                    invalid_invariants_and_reason.append((inv, data[0], data[1], data[2]))
                    has_counterexample = True
            else:
                valid_invariants.add(inv)

    if not has_counterexample:
        new_try_count = 0

    content = f"invalid invariants: {json.dumps(invalid_invariants_and_reason)}"
    msgs.append(
        ToolMessage(
            content=content,
            tool_call_id="call_task12_smt_solver",
            name="task12_smt_solver",
        )
    )

    task12_data["has_counterexample"] = has_counterexample
    task12_data["llm_gen"] = llm_gen
    task12_data["try_count"] = new_try_count
    task12_data["valid_invariants"] = valid_invariants
    task12_data["msgs"] = msgs
    if has_counterexample:
        task12_data["counterexamples"] = invalid_invariants_and_reason

    return {
        "task12_data": task12_data,
    }
