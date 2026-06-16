import re
from nodes.common import (
    AgentState, get_func_subject_dir, get_tmp_code_path,
    get_pre_task_z3_template_path, get_post_task_z3_template_path, 
    get_verify_dir, get_loop_subject_dir, get_err_log_path, LoopNode, IfNode, TransNode,
    conjuct_invariants,dprint, get_current_code
)
from common import (
    # TY_IF, TY_LOOP,
    # TY_TRANSFORM, TY_IF_COND,
    node2str,Node, dprint
)
from langchain_core.messages import SystemMessage
import os

from prompt_templates import loop_code_prompt

def find_vars_in_cond(cond:str, all_vars:list):
    ret_vars = set()
    for var in all_vars:
        if re.search(rf'\b{var}\b', cond):
            ret_vars.add(var)
    return ret_vars

def find_counterexample_vars(data:list, counterexample_vars:set, all_vars:list):
    for item in data:
        if isinstance(item, TransNode):
            counterexample_vars.add(item.left_var)
        elif isinstance(item, IfNode):
            for branch in item.branches:
                vars_in_cond = find_vars_in_cond(branch[0], all_vars)
                counterexample_vars |= vars_in_cond
                find_counterexample_vars(branch[1], counterexample_vars, all_vars)
        elif isinstance(item, LoopNode):
            # print(item[-1])
            vars_in_cond = find_vars_in_cond(item.guard, all_vars)
            counterexample_vars |= vars_in_cond
            find_counterexample_vars(item.body, counterexample_vars, all_vars)


# 在只取目标节点之前的代码的情况下，
# 将已知循环不变式的内层循环变为循环不变式,注释，外层保留
# def get_current_code(config, func_name:str, func_node: Node,loop_ir_node: LoopNode|None, loop_nodes:list[Node], func_loops_invs:list[list[str]]):
#     def is_loop_node(_node: Node) -> bool:
#         return _node.type in ("for_statement", "while_statement", "do_statement")

#     def __get_current_code(source_bytes, invs_map, target_loop_node, target_loop_assert, cur_node:Node, parts=None, finished=None):
#         # if finished[0]:
#         #     return

#         # If the current node is a loop with known invariants, insert them.
#         if cur_node in invs_map:
#             tmp_parts = []
#             for inv in invs_map[cur_node]:
#                 tmp_parts.append(f"({inv})")
#             loop_guard = node2str(cur_node.child_by_field_name("condition"))
#             tmp_parts.append(f"!({loop_guard})")
#             assume_str = "//@ ASSUME(" + " && ".join(tmp_parts) + ")"
#             parts.append(assume_str)

#             # If this node is the target, we are done.
#             if cur_node == target_loop_node:
#                 finished[0] = True
#             return # Stop traversing into this loop's children

       
#         if target_loop_node is not None:
#             is_ancestor = (cur_node.start_byte <= target_loop_node.start_byte and
#                            cur_node.end_byte >= target_loop_node.end_byte)
#             # Pruning: If the current node is a loop that is NOT an ancestor of the target,
#             # we don't need to traverse it. We just return.
#             if is_loop_node(cur_node) and not is_ancestor and cur_node != target_loop_node:
#                 return

#         # Standard recursive traversal to rebuild the code from the AST
#         if cur_node.child_count == 0:
#             parts.append(cur_node.text.decode('utf8'))
#         else:
#             prev_child_end = cur_node.start_byte
#             base_offset = func_node.start_byte
#             for i, child in enumerate(cur_node.children):
#                 # 添加上一个结点和当前结点之间的换行和缩进
#                 indent:str = source_bytes[prev_child_end-base_offset:child.start_byte-base_offset].decode('utf8')
#                 parts.append(indent)
#                 if not finished[0] and child == target_loop_node:
#                     parts.append(f"TARGET_LOOP:")
#                 __get_current_code(source_bytes, invs_map, target_loop_node, target_loop_assert, child, parts, finished)
#                 # if finished[0]:
#                     # if child == target_loop_node and target_loop_assert:
#                     #     parts.append("\n"+indent.lstrip("\n").rstrip("\n"))
#                     #     parts.append(f"//@ assert({target_loop_assert})")
#                     # return
#                 prev_child_end = child.end_byte
#             # Append any remaining text after the last child
#             parts.append(source_bytes[prev_child_end-base_offset:cur_node.end_byte-base_offset].decode('utf8'))

#         # Final check if the current node itself is the target
#         if cur_node == target_loop_node:
#             finished[0] = True

#     target_node = None
#     loop_id = None
#     target_loop_post_assert = None

#     # Determine the target_node only if loop_data is provided
#     if loop_ir_node is not None:
#         loop_id = loop_ir_node.loop_id
#         target_node = loop_nodes[loop_id]
#         target_loop_post_assert = loop_ir_node.post_condition

#     # Map loop nodes to their invariants for easy lookup
#     invs_map = dict()
#     # print("%"*50)
#     # print(loops_invs)
#     # print(loop_id_dict)
#     # dprint(func_loops_invs)
#     for _loop_id, loop_invs in enumerate(func_loops_invs):
#         # dprint(_loop_id, loop_invs)
#         invs_map[loop_nodes[_loop_id]] = loop_invs
#     # dprint(invs_map)
    

#     parts = []
#     __get_current_code(func_node.text, invs_map, target_node, target_loop_post_assert, func_node, parts, finished=[False])
#     final_code = "".join(parts)

#     if loop_id is not None:
#         filename = f"LOOP_{loop_id}.c"
#         tmp_code_path = get_tmp_code_path(config, func_name, loop_id)
#     else:
#         subject_dir = get_func_subject_dir(config, func_name)
#         tmp_code_path = os.path.join(subject_dir, "FINAL_code.c")
#     with open(tmp_code_path, "w") as f:
#         f.write(final_code)

#     dprint(tmp_code_path)
#     dprint(final_code)
#     # exit()
        
#     return final_code

def next_loop(state: AgentState, config)->AgentState:
    func_data = state["func_data"]
    loop_data = state["loop_data"]

    path_to_loops = func_data["path_to_loops"]
    func_node = func_data["cur_node"]
    func_name = func_data["cur_name"]
    loop_nodes = func_data["loop_nodes"]
    loops_invs = func_data["loops_invs"]
    var_type_dict = func_data["var_type_dict"]

    pre_loop_id = loop_data["cur_id"]


    loop_ir_nodes = []
    for p in path_to_loops:
        ir_node = p[-1]
        loop_ir_nodes.append(ir_node)
    
    
    # print("******",path_to_cur_handled_loop)
    # for p in path_to_loops:
    #     print("====",p)

    cur_loop_id = pre_loop_id + 1
    # cur_loop_id = 3
    # loops_invs = [
    #     ["inv0"],
    #     ["inv1"],
    #     ["inv2"],
    #     ["inv3"],
    #     ["inv4"],
    #     ["inv5"]
    # ]

    if cur_loop_id == len(path_to_loops):
        get_current_code(
            config, 
            func_name, 
            func_node, 
            None, 
            loop_nodes, 
            loop_ir_nodes,
            loops_invs,
            False
        )
        loop_data["cur_id"] = cur_loop_id
        return {"loop_data": loop_data}
    
    path_to_cur_handled_loop = path_to_loops[cur_loop_id]

    # dprint(path_to_cur_handled_loop)

    loop_ir_node:LoopNode = path_to_cur_handled_loop[-1]
    has_assert = loop_ir_node.post_condition != None

    counterexample_vars = set()
    find_counterexample_vars(loop_ir_node.body, counterexample_vars, var_type_dict.keys())

    get_loop_subject_dir(config, func_name, cur_loop_id, True)
    get_tmp_code_path(config, func_name, cur_loop_id, True)
    get_pre_task_z3_template_path(config, func_name, cur_loop_id, True)
    # 没有assert就不创建
    if has_assert:
        get_post_task_z3_template_path(config, func_name, cur_loop_id, True)
    get_verify_dir(config, func_name, cur_loop_id, True)
    get_err_log_path(config, func_name, cur_loop_id, True)

    true_func_code = get_current_code(
        config, 
        func_name, 
        func_node, 
        loop_ir_node, 
        loop_nodes, 
        loop_ir_nodes,
        loops_invs,
        True
    )

    loops_key_vars = func_data["loops_key_vars"]
    print(loops_key_vars)
    key_vars = loops_key_vars[cur_loop_id]

    loop_key_vars_str = ",".join([f"`{key_var}`" for key_var in key_vars])

    

    prompt = loop_code_prompt.format(
        func_code=true_func_code,
        loop_key_vars=loop_key_vars_str
    )
    # print(prompt)

    
    loop_sys_msg = SystemMessage(content=prompt)
    loops_counterexample_vars = func_data["loops_counterexample_vars"]
    loops_counterexample_vars.append(counterexample_vars)

    loop_data["cur_id"] = cur_loop_id
    loop_data["key_vars"] = key_vars
    loop_data["path_to_loop"] = path_to_cur_handled_loop
    loop_data["loop_code_msg"] = loop_sys_msg
    loop_data["counterexample_vars"] = counterexample_vars

    # 将这个提示词保存
    subject_dir = get_loop_subject_dir(config, func_data["cur_name"], loop_data["cur_id"])
    log_file = os.path.join(subject_dir, "pre_code_prompt.log")
    with open(log_file, "w") as f:
        f.write(loop_data["loop_code_msg"].pretty_repr())

    return {
        "loop_data": loop_data,
    }
    
    # return {
    #     "loop_id": cur_loop_id,
    #     "loop_key_vars": key_vars, 
    #     "loops_key_vars": loops_key_vars,
    #     "loop_sys_msg": loop_sys_msg,
    #     "llm_gen_invariants_each": dict(),
    #     "llm_gen_invariants_combined": list(),
    #     "invariants_with_counterexample_each": dict(),
    #     "invariants_with_counterexample_combined": dict(),
    #     "invariants_each": invariants_each,
    #     "invariants_combined": set(),
    #     "messages_each": list(),
    #     "messages_combined": list(),
    #     "has_assert": has_assert,
    # }