import json
import os
from nodes.common import (
    AgentState, LoopNode, conjuct_invariants, dprint, trans_invariant, 
    get_verify_dir, get_err_log_path, get_pre_task_z3_template_path, get_experiment_switches
)
from utils.solve_smt import solve_smt as _solve_smt
from langchain_core.messages import ToolMessage
from common import unimplement
from utils.fol_parser import replace_old_for_solve

def __solve(config, invariant:str, valid_invariants, func_name, loop_id, key_vars, ssa_dict, idx, new_try_count:int):
    verify_dir = get_verify_dir(config, func_name, loop_id)
    template_file_path = get_pre_task_z3_template_path(config, func_name, loop_id)
    err_log_path = get_err_log_path(config, func_name, loop_id)
    # fol转为z3的格式
    conj_inv = conjuct_invariants(valid_invariants | {invariant})
    try:
        inv_replaced_old = replace_old_for_solve(conj_inv, key_vars)
        quantifier_binder_var_init_code, final_invariant, z3_invariant = trans_invariant(inv_replaced_old, key_vars, ssa_dict)
    except Exception as e:
        with open(err_log_path, "a") as f:
            f.write(f"{e}\nWhen solve_post parsing.\n\n")
        return False,None,None
    with open(template_file_path, "r") as f:
        solve_template = f.read()
    filled_solve_code = solve_template.format(quantifier_binder_var_init_code, invariant, z3_invariant)

    prefix = f"post-step1-try_{new_try_count}-idx_{idx}"
    filled_solve_file = os.path.join(verify_dir,f"{prefix}.py")
    dprint(filled_solve_file)
    with open(filled_solve_file, "w") as f:
        f.write(filled_solve_code)
    try:
        valid, data, duration = _solve_smt(filled_solve_file)
    except Exception as e:
        with open(err_log_path, "a") as f:
            f.write(f"{e}\nWhen solve_post solving.\n\n")
        return False, None, None
    return True, valid, data

def solve_smt_post_single(state: AgentState, config) -> AgentState:
    task3_data = state["task3_data"]
    loop_data = state["loop_data"]
    func_data = state["func_data"]

    func_name = func_data["cur_name"]
    path_to_loop = loop_data["path_to_loop"]
    key_vars = loop_data["key_vars"]
    ssa_dict = loop_data["ssa_dict_after_loop"]
    llm_gen = task3_data["llm_gen"]
    valid_invariants = task3_data["valid_invariants"]
    msgs = task3_data["msgs"]

    cur_try_count = task3_data["try_count"]
    loop_ir_node:LoopNode = path_to_loop[-1]
    
    has_counterexample = False
    invalid_invariants_and_reason = list()
    err_invs = set()
    iterative = get_experiment_switches(config)["enable_iterative"]
    idx = -1
    while True:
        new_invariants_found = False
        current_candidates = [inv for inv in llm_gen if inv not in valid_invariants]

        if len(current_candidates) == 0:
            break

        current_invalid_invariants = []
        for inv in current_candidates:
            if inv in valid_invariants:
                continue
            idx += 1
            tmp_invariant = inv
            no_err, valid, data = __solve(
                config, tmp_invariant, valid_invariants, func_name,
                loop_ir_node.loop_id, key_vars,
                ssa_dict, idx, cur_try_count,
            )
            if not no_err:
                err_invs.add(inv)
                continue
            if not valid:
                if isinstance(data, str):
                    # 大语言模型的问题或者我的转换的问题
                    pass
                elif isinstance(data, tuple):
                    current_invalid_invariants.append((inv, data[0], data[1], data[2]))
                    has_counterexample = True
                else:
                    print(data)
                    raise NotImplementedError()
            else:
                valid_invariants.add(inv)
                new_invariants_found = True

        invalid_invariants_and_reason = current_invalid_invariants

        llm_gen = set([inv for inv in llm_gen if inv not in err_invs])
        if not new_invariants_found or not iterative:
            break

    content = f"invalid invariants: {json.dumps(invalid_invariants_and_reason)}"
    dprint(content)
    msgs.append(
        ToolMessage(
            content=content,
            tool_call_id="call_step1_post_smt_solver",
            name="post_step1_smt_solver",
        )
    )
    
    # 去除所有格式错误的不变式
    task3_data["has_counterexample"] = has_counterexample
    task3_data["llm_gen"] = llm_gen
    task3_data["valid_invariants"] = valid_invariants
    task3_data["msgs"] = msgs
    return {
        "task3_data": task3_data,
    }