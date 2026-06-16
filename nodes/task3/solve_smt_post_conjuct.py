import json
import os
import traceback
from nodes.common import (
    AgentState, LoopNode, conjuct_invariants, dprint, trans_invariant, 
    get_verify_dir, get_err_log_path, get_post_task_z3_template_path,
)
from utils.solve_smt import solve_smt as _solve_smt
from langchain_core.messages import ToolMessage
from common import unimplement
from utils.fol_parser import replace_old_for_solve

def __solve(config, invariant:str, func_name, loop_id, key_vars, ssa_dict, new_try_count:int):
    verify_dir = get_verify_dir(config, func_name, loop_id)
    template_file_path = get_post_task_z3_template_path(config, func_name, loop_id)
    err_log_path = get_err_log_path(config, func_name, loop_id)
    # fol转为z3的格式
    try:
        inv_replaced_old = replace_old_for_solve(invariant, key_vars)
        quantifier_binder_var_init_code, final_invariant, z3_invariant = trans_invariant(inv_replaced_old, key_vars, ssa_dict)
    except Exception as e:
        traceback.print_exc()
        with open(err_log_path, "a") as f:
            f.write(f"{e}\nWhen solve_post parsing.\n\n")
        return False,None,None
    with open(template_file_path, "r") as f:
        solve_template = f.read()
    filled_solve_code = solve_template.format(quantifier_binder_var_init_code, invariant, z3_invariant)

    prefix = f"post-step2-try_{new_try_count}"
    filled_solve_file = os.path.join(verify_dir,f"{prefix}.py")
    with open(filled_solve_file, "w") as f:
        # dprint(filled_solve_file)
        f.write(filled_solve_code)
    try:
        valid, data, duration = _solve_smt(filled_solve_file)
    except Exception as e:
        traceback.print_exc()
        with open(err_log_path, "a") as f:
            f.write(f"{e}\nWhen solve_post solving.\n\n")
        return False, None, None
    return True, valid, data

def solve_smt_post_conjuct(state: AgentState, config) -> AgentState:
    task3_data = state["task3_data"]
    loop_data = state["loop_data"]
    func_data = state["func_data"]

    func_name = func_data["cur_name"]
    path_to_loop = loop_data["path_to_loop"]
    key_vars = loop_data["key_vars"]
    ssa_dict = loop_data["ssa_dict_after_loop"]
    # llm_gen = task3_data["llm_gen"]
    valid_invariants = task3_data["valid_invariants"]
    msgs = task3_data["msgs"]

    new_try_count = task3_data["try_count"]+1
    loop_ir_node:LoopNode = path_to_loop[-1]
    
    has_counterexample = False
    counterexample_and_reason = None
    
    conj_inv = conjuct_invariants(valid_invariants)

    no_err, valid, data = __solve(
        config, conj_inv, func_name, loop_ir_node.loop_id, key_vars, ssa_dict,
        new_try_count
    )
    if not no_err:
        unimplement(f"format err or timeout in post solve: {conj_inv}")
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
        msg_content = f"invalid invariants: {conj_inv}\n{counterexample_and_reason[0]}\n{counterexample_and_reason[2]}"
    else:
        msg_content = "valid"
    dprint(msg_content)
    msgs.append(
        ToolMessage(
            content=msg_content,
            tool_call_id="call_step2_post_smt_solver",
            name="post_step2_smt_solver",
        )
    )
    # 准备返回值
    task3_data["has_counterexample"] = has_counterexample
    task3_data["try_count"] = new_try_count
    if has_counterexample:
        task3_data["counterexample"] = counterexample_and_reason
    task3_data["msgs"] = msgs
    return {
        "task3_data": task3_data,
    }