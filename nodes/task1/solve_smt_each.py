import json
import os
import traceback
from nodes.common import AgentState, trans_invariant, get_verify_dir, get_err_log_path, get_pre_task_z3_template_path, conjuct_invariants, get_experiment_switches
from utils.solve_smt import solve_smt as _solve_smt
from langchain_core.messages import ToolMessage
from common import dprint
from nodes.common import LoopNode
from utils.fol_parser import replace_old_for_solve

def __solve(config, invariant:str, func_name, loop_id, key_vars, ssa_dict, idx:int, new_try_count:int, valid_invariants:dict[str,set[str]]):
    verify_dir = get_verify_dir(config, func_name, loop_id)
    template_file_path = get_pre_task_z3_template_path(config, func_name, loop_id)
    err_log_path = get_err_log_path(config, func_name, loop_id)
    # fol转为z3的格式
    try:
        valids = set()
        for __,v in valid_invariants.items():
            for vv in v:
                valids.add(vv)
        new_invs = [invariant] + list(valids)
        new_inv = conjuct_invariants(new_invs)
        inv_replaced_old = replace_old_for_solve(new_inv, key_vars)
        quantifier_binder_var_init_code, final_invariant, z3_invariant = trans_invariant(inv_replaced_old, key_vars, ssa_dict)
    except Exception as e:
        with open(err_log_path, "a") as f:
            f.write("When solve_each parsing:\n")
            traceback.print_exc(file=f)
            f.write("\n\n")
        return False,None,None
    with open(template_file_path, "r") as f:
        solve_template = f.read()
    filled_solve_code = solve_template.format(quantifier_binder_var_init_code, invariant, z3_invariant)
    
    prefix = f"pre-each-try_{new_try_count}-idx_{idx}"
    filled_verify_file = os.path.join(verify_dir,f"{prefix}.py")
    with open(filled_verify_file, "w") as f:
        f.write(filled_solve_code)
    try:
        valid, data, duration = _solve_smt(filled_verify_file)
    except Exception as e:
        with open(err_log_path, "a") as f:
            f.write(f"{e}\nWhen solve_each solving.\n\n")
        return False, None, None
    return True, valid, data

def solve_smt_each(state: AgentState, config) -> AgentState:
    task1_data = state["task1_data"]
    loop_data = state["loop_data"]
    func_data = state["func_data"]

    func_name = func_data["cur_name"]
    path_to_loop = loop_data["path_to_loop"]
    key_vars = loop_data["key_vars"]
    ssa_dict = loop_data["ssa_dict_before_loop"]
    llm_gen = task1_data["llm_gen"]
    valid_invariants = task1_data["valid_invariants"]
    msgs = task1_data["msgs"]
   
    loop_ir_node:LoopNode = path_to_loop[-1]
    new_try_count = task1_data["try_count"] + 1

    has_counterexample = False
    all_invalid_invariants = dict()
    err_invs = dict()
    idx = -1
    iterative = get_experiment_switches(config)["enable_iterative"]

    # for key_var, invariants in llm_gen.items():
    #     invalid_invariants_and_reason = list()
    #     for inv in invariants:
    #         if inv in valid_invariants[key_var]:
    #             continue
    #         idx += 1
    #         tmp_invariant = inv
    #         no_err, valid, data = __solve(
    #             config, tmp_invariant, func_name, 
    #             loop_ir_node.loop_id, key_vars,
    #             ssa_dict, idx, new_try_count,  valid_invariants,
    #         )
    #         if not no_err:
    #             if err_invs.get(key_var) is None:
    #                 err_invs[key_var] = set()
    #             err_invs[key_var].add(inv)
    #             continue
    #         if not valid:
    #             if isinstance(data, str):
    #                 # 大语言模型的问题或者我的转换的问题
    #                 raise Exception(data)
    #             elif isinstance(data, tuple):
    #                 invalid_invariants_and_reason.append( (inv, data[0], data[1], data[2]) )
    #                 has_counterexample = True
    #                 # 处理一下
    #             else:
    #                 dprint(data)
    #                 raise NotImplementedError()
    #         else:
    #             valid_invariants[key_var].add(inv)
    #     if len(invalid_invariants_and_reason) > 0:
    #         all_invalid_invariants[key_var] = invalid_invariants_and_reason
    # # 去除所有格式错误的不变式
    # for key_var in err_invs:
    #     llm_gen[key_var] = set([inv for inv in llm_gen[key_var] if inv not in err_invs[key_var]])

    while True:  # 添加外层循环，直到没有新的不变式被验证为有效
        new_invariants_found = False
        
        # 创建当前迭代需要检查的候选列表
        current_candidates = {}
        for key_var, invariants in llm_gen.items():
            # 只考虑尚未验证有效的不变式
            current_candidates[key_var] = [inv for inv in invariants if inv not in valid_invariants.get(key_var, set())]
        
        # 如果没有待检查的候选，退出循环
        if all(len(candidates) == 0 for candidates in current_candidates.values()):
            break
        
        for key_var, invariants in current_candidates.items():
            invalid_invariants_and_reason = list()
            
            for inv in invariants:
                # 再次检查是否已被其他迭代验证为有效（防止并发修改的问题）
                if inv in valid_invariants.get(key_var, set()):
                    continue
                    
                idx += 1
                tmp_invariant = inv
                no_err, valid, data = __solve(
                    config, tmp_invariant, func_name, 
                    loop_ir_node.loop_id, key_vars,
                    ssa_dict, idx, new_try_count,  valid_invariants,
                )
                
                if not no_err:
                    if err_invs.get(key_var) is None:
                        err_invs[key_var] = set()
                    err_invs[key_var].add(inv)
                    continue
                    
                if not valid:
                    if isinstance(data, str):
                        # 大语言模型的问题或者我的转换的问题
                        raise Exception(data)
                    elif isinstance(data, tuple):
                        invalid_invariants_and_reason.append((inv, data[0], data[1], data[2]))
                        has_counterexample = True
                        # 处理一下
                    else:
                        dprint(data)
                        raise NotImplementedError()
                else:
                    # 发现新的有效不变式
                    if key_var not in valid_invariants:
                        valid_invariants[key_var] = set()
                    valid_invariants[key_var].add(inv)
                    new_invariants_found = True
            
            # 记录本轮发现的无效不变式
            if len(invalid_invariants_and_reason) > 0:
                if key_var not in all_invalid_invariants:
                    all_invalid_invariants[key_var] = []
                all_invalid_invariants[key_var].extend(invalid_invariants_and_reason)
        
        # 去除所有格式错误的不变式
        for key_var in err_invs:
            if key_var in llm_gen:
                llm_gen[key_var] = set([inv for inv in llm_gen[key_var] if inv not in err_invs[key_var]])
        
        # 如果没有找到新的有效不变式，退出循环
        if not new_invariants_found or not iterative:
            break


    if not has_counterexample:
        new_try_count = 0
    content = f"invalid invariants: {json.dumps(all_invalid_invariants)}"
    dprint(content)
    msgs.append(
        ToolMessage(
            content=content,
            tool_call_id="call_each_var_smt_solver",
            name="each_smt_solver",
        )
    )
    # 准备返回值
    task1_data["has_counterexample"] = has_counterexample
    task1_data["llm_gen"] = llm_gen
    task1_data["try_count"] = new_try_count
    task1_data["valid_invariants"] = valid_invariants
    task1_data["msgs"] = msgs

    if has_counterexample:
        task1_data["counterexamples"] = all_invalid_invariants
    return {
        "task1_data": task1_data,
    }