import json
import os
from common import dprint
from nodes.common import AgentState, LoopNode, trans_invariant, get_verify_dir, get_err_log_path, get_pre_task_z3_template_path, conjuct_invariants
from utils.solve_smt import solve_smt as _solve_smt
from langchain_core.messages import ToolMessage
from utils.fol_parser import replace_old_for_solve
import traceback

def __solve(config, invariant:str, func_name, loop_id, key_vars, ssa_dict, idx:int, new_try_count:int, valid_invariants:set[str]):
    verify_dir = get_verify_dir(config, func_name, loop_id)
    template_file_path = get_pre_task_z3_template_path(config, func_name, loop_id)
    err_log_path = get_err_log_path(config, func_name, loop_id)
    # fol转为z3的格式
    try:
        new_invs = [invariant] + list(valid_invariants)
        new_inv = conjuct_invariants(new_invs)
        inv_replaced_old = replace_old_for_solve(new_inv, key_vars)
        dprint(inv_replaced_old)
        quantifier_binder_var_init_code, final_invariant, z3_invariant = trans_invariant(inv_replaced_old, key_vars, ssa_dict)
    except Exception as e:
        with open(err_log_path, "a") as f:
            f.write("When solve_combined parsing:\n")
            traceback.print_exc(file=f)
            f.write("\n\n")
        return False,None,None
    with open(template_file_path, "r") as f:
        solve_template = f.read()
    filled_solve_code = solve_template.format(quantifier_binder_var_init_code, invariant, z3_invariant)

    prefix = f"pre-combined-try_{new_try_count}-idx_{idx}"
    filled_solve_file = os.path.join(verify_dir,f"{prefix}.py")
    with open(filled_solve_file, "w") as f:
        f.write(filled_solve_code)
    try:
        valid, data, duration = _solve_smt(filled_solve_file)
    except Exception as e:
        with open(err_log_path, "a") as f:
            f.write(f"{e}\nWhen solve_combined solving.\n\n")
        return False, None, None
    return True, valid, data

def solve_smt_combined(state: AgentState, config) -> AgentState:
    task2_data = state["task2_data"]
    loop_data = state["loop_data"]
    func_data = state["func_data"]

    func_name = func_data["cur_name"]
    path_to_loop = loop_data["path_to_loop"]
    key_vars = loop_data["key_vars"]
    ssa_dict = loop_data["ssa_dict_before_loop"]
    llm_gen = task2_data["llm_gen"]
    valid_invariants = task2_data["valid_invariants"]
    msgs = task2_data["msgs"]

    loop_ir_node:LoopNode = path_to_loop[-1]
    new_try_count = task2_data["try_count"] + 1

    has_counterexample = False
    invalid_invariants_and_reason = list()
    err_invs = set()

    idx = -1

    for inv in llm_gen:
        if inv in valid_invariants:
            continue
        idx += 1
        tmp_invariant = inv
        no_err, valid, data = __solve(
            config, tmp_invariant, func_name,
            loop_ir_node.loop_id, key_vars,
            ssa_dict ,idx, new_try_count, valid_invariants
        )
        if not no_err:
            err_invs.add(inv)
            continue
        if not valid:
            if isinstance(data, str):
                # 大语言模型的问题或者我的转换的问题
                pass
            elif isinstance(data, tuple):
                invalid_invariants_and_reason.append( (inv, data[0], data[1], data[2]) )
                has_counterexample = True
            else:
                print(data)
                raise NotImplementedError()
        else:
            valid_invariants.add(inv)
            
    # 去除所有格式错误的不变式
    llm_gen = set([inv for inv in llm_gen if inv not in err_invs])
    if not has_counterexample:
        new_try_count = 0
    content = f"invalid invariants: {json.dumps(invalid_invariants_and_reason)}"
    msgs.append(
        ToolMessage(
            content=content,
            tool_call_id="call_combined_smt_solver",
            name="combined_smt_solver",
        )
    )
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