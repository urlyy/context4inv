import os
from pathlib import Path
from nodes.common import (
    AgentState, get_pre_task_z3_template_path, 
    get_post_task_z3_template_path, dprint
)
from utils.solve_smt import path2z3

def generate_z3_template(state: AgentState, config) -> AgentState:
    loop_data = state["loop_data"]
    func_data = state["func_data"]
    
    loop_key_vars = loop_data["key_vars"]
    loop_id = loop_data["cur_id"]
    path_to_loop = loop_data["path_to_loop"]
    
    func_name = func_data["cur_name"]
    loops_key_vars = func_data["loops_key_vars"]
    var_type_dict = func_data["var_type_dict"]
    func_loops_invs = func_data["loops_invs"]

    pre_task_template_path = get_pre_task_z3_template_path(config, func_name, loop_id)
    post_task_template_path = get_post_task_z3_template_path(config, func_name, loop_id)
    

    func_spec_dict = None
    some_data = path2z3(
        path_to_loop, loop_key_vars, var_type_dict, func_loops_invs, loops_key_vars, 
        func_spec_dict, pre_task_template_path, post_task_template_path
    )
    ssa_dict_after_pre, ssa_dict_before_loop, ssa_dict_after_trans, ssa_dict_after_loop = some_data[1]
    loop_data["ssa_dict_after_pre"] = ssa_dict_after_pre
    loop_data["ssa_dict_before_loop"] = ssa_dict_before_loop
    loop_data["ssa_dict_after_trans"] = ssa_dict_after_trans
    loop_data["ssa_dict_after_loop"] = ssa_dict_after_loop

    ssa_dicts = [loop_data["ssa_dict_after_pre"], loop_data["ssa_dict_before_loop"], loop_data["ssa_dict_after_trans"], loop_data["ssa_dict_after_loop"]]
    func_data["loops_ssa_dicts"].append(ssa_dicts)

    dprint(pre_task_template_path)

    # exit()

    return {
        "loop_data":loop_data,
        "func_data": func_data,
    }