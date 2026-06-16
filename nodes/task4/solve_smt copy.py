import json
import os
from nodes.common import (
    AgentState, LoopNode, conjuct_invariants, trans_invariant, get_verify_dir, get_err_log_path, 
    get_pre_task_z3_template_path, get_post_task_z3_template_path,dprint
)
from utils.solve_smt import path2z3, solve_smt as _solve_smt
from langchain_core.messages import ToolMessage

def __solve(config, invariant:str, has_assert:bool, func_name, loop_id, key_vars, ssa_dict, new_try_count:int):
    verify_dir = get_verify_dir(config, func_name, loop_id)
    if has_assert:
        template_file_path = get_post_task_z3_template_path(config, func_name, loop_id)
    else:
        template_file_path = get_pre_task_z3_template_path(config, func_name, loop_id)
    err_log_path = get_err_log_path(config, func_name, loop_id)
    # fol转为z3的格式
    try:
        quantifier_binder_var_init_code, final_invariant, z3_invariant = trans_invariant(invariant, key_vars, ssa_dict)
    except Exception as e:
        with open(err_log_path, "a") as f:
            f.write(f"{e}\nWhen solve_combined parsing.\n\n")
        return False,None,None
    with open(template_file_path, "r") as f:
        solve_template = f.read()
    filled_solve_code = solve_template.format(quantifier_binder_var_init_code, invariant, z3_invariant)

    prefix = f"task4-try_{new_try_count}-loop_{loop_id}"
    filled_solve_file = os.path.join(verify_dir,f"{prefix}.py")
    dprint(filled_solve_file)
    with open(filled_solve_file, "w") as f:
        f.write(filled_solve_code)
    try:
        valid, data, duration = _solve_smt(filled_solve_file)
    except Exception as e:
        with open(err_log_path, "a") as f:
            f.write(f"{e}\nWhen solve_task4 solving.\n\n")
        return False, None, None
    return True, valid, data

def __check_fmt(config, invariant:str, func_name, loop_id, key_vars, ssa_dict, idx):
    verify_dir = get_verify_dir(config, func_name, loop_id)
    template_file_path = get_pre_task_z3_template_path(config, func_name, loop_id)
    err_log_path = get_err_log_path(config, func_name, loop_id)
    # fol转为z3的格式
    try:
        quantifier_binder_var_init_code, final_invariant, z3_invariant = trans_invariant(invariant, key_vars, ssa_dict)
    except Exception as e:
        with open(err_log_path, "a") as f:
            f.write(f"{e}\nWhen solve_combined parsing.\n\n")
        return False,None,None
    
    with open(template_file_path, "r") as f:
        solve_template = f.read()
    filled_solve_code = solve_template.format(quantifier_binder_var_init_code, invariant, z3_invariant)

    prefix = f"task4-fmt-test-{idx}"
    filled_solve_file = os.path.join(verify_dir,f"{prefix}.py")
    with open(filled_solve_file, "w") as f:
        f.write(filled_solve_code)

    try:
        valid, data, duration = _solve_smt(filled_solve_file)
    except Exception as e:
        with open(err_log_path, "a") as f:
            f.write(f"{e}\nWhen solve_task4 fmt checking.\n\n")
        return False, None, None
    return True, valid, data

# 把当前循环之后的全部求解一遍
def solve_smt(state: AgentState, config) -> AgentState:
    func_data = state["func_data"]
    task4_data = state["task4_data"]
    cur_loop_id = state["loop_data"]["cur_id"]

    func_name = func_data["cur_name"]
    
    loop_range = range(task4_data["smallest_modified_loop_id"], cur_loop_id+1)

    loops_invs = func_data["loops_invs"]
    var_type_dict = func_data["var_type_dict"]
    loops_key_vars = func_data["loops_key_vars"]

    msgs = task4_data["msgs"]

    cur_try_count = task4_data["try_count"]
    has_counterexample = False
    ce_reason, ce_data = None, None
    ce_loop_id = None

    llm_gen = task4_data["llm_gen"]


    idx = -1
    for tmp_loop_id in loop_range:
        path_to_loop = func_data["path_to_loops"][tmp_loop_id]
        key_vars = loops_key_vars[tmp_loop_id]
        ssa_dict = func_data["loops_ssa_dicts"][tmp_loop_id][0]

        loop_ir_node:LoopNode = path_to_loop[-1]

        pre_task_template_path = get_pre_task_z3_template_path(config, func_name, tmp_loop_id)
        post_task_template_path = get_post_task_z3_template_path(config, func_name, tmp_loop_id)
        
        # 
        func_spec_dict = None
        # renew z3 template for this loop, only use invariant belong to before loops
        _ = path2z3(
            path_to_loop, key_vars, var_type_dict, loops_invs, loops_key_vars, 
            func_spec_dict, pre_task_template_path, post_task_template_path
        )

        new_invs_for_this_loop = llm_gen[f"LOOP_{tmp_loop_id}"]

        
        # 先保留能用的
        valid_invariants = set()
        for inv in new_invs_for_this_loop:
            idx += 1
            tmp_invariant = inv
            no_err, _, _ = __check_fmt(
                config, tmp_invariant, func_name,
                loop_ir_node.loop_id, key_vars,
                ssa_dict, idx
            )
            if not no_err:
                continue
            valid_invariants.add(inv)
        loops_invs[tmp_loop_id] = valid_invariants
        
        # 再统一求一下
        conj_inv = conjuct_invariants(valid_invariants)
        _, valid, data = __solve(
            config, conj_inv, loop_ir_node.post_condition!=None, func_name, loop_ir_node.loop_id, 
            key_vars, ssa_dict, cur_try_count
        )

        if valid:
            continue

        has_counterexample = True
        ce_reason, ce_data = data
        ce_loop_id = tmp_loop_id
        break
    
    func_data["loops_invs"] = loops_invs
    task4_data["has_counterexample"] = has_counterexample
    if has_counterexample:
       task4_data["ce_and_loop_id"] = ((ce_reason, ce_data), ce_loop_id)

    return {
        "func_data": func_data,
        "task4_data": task4_data,
    }
        
        # 去除所有格式错误的不变式
        # llm_gen = set([inv for inv in llm_gen if inv not in err_invs])
        # if not has_counterexample:
        #     new_try_count = 0
        # content = f"invalid invariants: {json.dumps(invalid_invariants_and_reason)}"
        # msgs.append(
        #     ToolMessage(
        #         content=content,
        #         tool_call_id="call_combined_smt_solver",
        #         name="combined_smt_solver",
        #     )
        # )
    # 准备返回值
    task2_data["has_counterexample"] = has_counterexample
    task2_data["llm_gen"] = llm_gen
    task2_data["try_count"] = new_try_count
    task2_data["valid_invariants"] = valid_invariants
    if has_counterexample:
        task2_data["counterexamples"] = invalid_invariants_and_reason
    task2_data["msgs"] = msgs
    return {
        "task2_data": task2_data,
    }
    