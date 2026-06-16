import json
import os
from common import unimplement
from nodes.common import (
    AgentState, LoopNode, conjuct_invariants, trans_invariant, get_verify_dir, get_err_log_path, 
    get_pre_task_z3_template_path, get_post_task_z3_template_path,dprint
)
from utils.solve_smt import path2z3, solve_smt as _solve_smt
from langchain_core.messages import ToolMessage
from utils.fol_parser import replace_old_for_solve

# def __solve(config, invariant:str, has_assert:bool, func_name, loop_id, key_vars, ssa_dict, new_try_count:int):
#     verify_dir = get_verify_dir(config, func_name, loop_id)
#     if has_assert:
#         template_file_path = get_post_task_z3_template_path(config, func_name, loop_id)
#     else:
#         template_file_path = get_pre_task_z3_template_path(config, func_name, loop_id)
#     err_log_path = get_err_log_path(config, func_name, loop_id)
#     # fol转为z3的格式
#     try:
#         quantifier_binder_var_init_code, final_invariant, z3_invariant = trans_invariant(invariant, key_vars, ssa_dict)
#     except Exception as e:
#         with open(err_log_path, "a") as f:
#             f.write(f"{e}\nWhen solve_combined parsing.\n\n")
#         return False,None,None
#     with open(template_file_path, "r") as f:
#         solve_template = f.read()
#     filled_solve_code = solve_template.format(quantifier_binder_var_init_code, invariant, z3_invariant)

#     prefix = f"task4-try_{new_try_count}-loop_{loop_id}"
#     filled_solve_file = os.path.join(verify_dir,f"{prefix}.py")
#     dprint(filled_solve_file)
#     with open(filled_solve_file, "w") as f:
#         f.write(filled_solve_code)
#     try:
#         valid, data, duration = _solve_smt(filled_solve_file)
#     except Exception as e:
#         with open(err_log_path, "a") as f:
#             f.write(f"{e}\nWhen solve_task4 solving.\n\n")
#         return False, None, None
#     return True, valid, data


def __solve_single(config, invariant:str, valid_invariants, has_assert:bool, func_name, loop_id, key_vars, ssa_dict, idx, new_try_count:int):
    verify_dir = get_verify_dir(config, func_name, loop_id)
    if has_assert:
        template_file_path = get_post_task_z3_template_path(config, func_name, loop_id)
    else:
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

    prefix = f"task4-single-try_{new_try_count}-loop_{loop_id}"
    filled_solve_file = os.path.join(verify_dir,f"{prefix}.py")
    dprint(filled_solve_file)
    with open(filled_solve_file, "w") as f:
        f.write(filled_solve_code)
    try:
        valid, data, duration = _solve_smt(filled_solve_file)
    except Exception as e:
        with open(err_log_path, "a") as f:
            f.write(f"{e}\nWhen solve_task4_single solving.\n\n")
        return False, None, None
    return True, valid, data

def __solve_conjuct(config, invariant:str, has_assert:bool, func_name, loop_id, key_vars, ssa_dict, new_try_count:int):
    verify_dir = get_verify_dir(config, func_name, loop_id)
    if has_assert:
        template_file_path = get_post_task_z3_template_path(config, func_name, loop_id)
    else:
        template_file_path = get_pre_task_z3_template_path(config, func_name, loop_id)
    err_log_path = get_err_log_path(config, func_name, loop_id)
    # fol转为z3的格式
    try:
        inv_replaced_old = replace_old_for_solve(invariant, key_vars)
        quantifier_binder_var_init_code, final_invariant, z3_invariant = trans_invariant(inv_replaced_old, key_vars, ssa_dict)
    except Exception as e:
        with open(err_log_path, "a") as f:
            f.write(f"{e}\nWhen solve_post parsing.\n\n")
        return False,None,None
    with open(template_file_path, "r") as f:
        solve_template = f.read()
    filled_solve_code = solve_template.format(quantifier_binder_var_init_code, invariant, z3_invariant)

    prefix = f"task4-conjuct-try_{new_try_count}-loop_{loop_id}"
    filled_solve_file = os.path.join(verify_dir,f"{prefix}.py")
    with open(filled_solve_file, "w") as f:
        # dprint(filled_solve_file)
        f.write(filled_solve_code)
    try:
        valid, data, duration = _solve_smt(filled_solve_file)
    except Exception as e:
        with open(err_log_path, "a") as f:
            f.write(f"{e}\nWhen solve_task4_conjuct solving.\n\n")
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

    dprint(llm_gen)


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
        valid_invariants = loops_invs[tmp_loop_id]
        # 先保留能用的
        candidate_invs = llm_gen[f"LOOP_{tmp_loop_id}"]
        for inv in candidate_invs:
            if inv in valid_invariants:
                continue
            idx += 1
            tmp_invariant = inv
            no_err, valid, data = __solve_single(
                config, tmp_invariant, valid_invariants, loop_ir_node.post_condition!=None, func_name, 
                loop_ir_node.loop_id, key_vars,
                ssa_dict, idx, cur_try_count,
            )
            if not no_err:
                continue
            if not valid:
                if isinstance(data, str):
                    # 大语言模型的问题或者我的转换的问题
                    pass
                elif isinstance(data, tuple):
                    # invalid_invariants_and_reason.append( (inv, data[0], data[1]) )
                    # has_counterexample = True
                    pass
                else:
                    print(data)
                    raise NotImplementedError()
            else:
                valid_invariants.add(inv)

        
        loops_invs[tmp_loop_id] = valid_invariants


        # conjuct test
        has_counterexample =False
        conj_inv = conjuct_invariants(valid_invariants)

        no_err, valid, data = __solve_conjuct(
            config, conj_inv, loop_ir_node.post_condition!=None, func_name, loop_ir_node.loop_id, key_vars, ssa_dict,
            cur_try_count
        )
        if not no_err:
            unimplement(f"format err in post solve: {conj_inv}")
        if not valid:
            if isinstance(data, str):
                # 大语言模型的问题或者我的转换的问题
                pass
            elif isinstance(data, tuple):
                counterexample_and_reason = data
                has_counterexample = True
            else:
                print(data)
                raise NotImplementedError()
        if has_counterexample:
            msg_content = f"invalid invariants for LOOP_{tmp_loop_id}: {conj_inv}\n{counterexample_and_reason[0]}\n{counterexample_and_reason[1]}\n{counterexample_and_reason[2]}"
        else:
            msg_content = "valid"

        if not valid:
            has_counterexample = True
            ce_reason, ce_is_unknown, ce_data = data
            ce_loop_id = tmp_loop_id
            break
    
    msgs.append(
        ToolMessage(
            content=msg_content,
            tool_call_id="call_task4_smt_solver",
            name="task4_smt_solver",
        )
    )
    func_data["loops_invs"] = loops_invs
    task4_data["has_counterexample"] = has_counterexample
    task4_data["msgs"] = msgs
    if has_counterexample:
       task4_data["ce_and_loop_id"] = ((ce_reason, ce_is_unknown, ce_data), ce_loop_id)

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