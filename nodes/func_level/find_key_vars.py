from common import dprint
from nodes.common import AgentState, LoopNode, IRNode, TransNode, IfNode, TransArrNode

def find_key_vars(state: AgentState) -> AgentState:
    func_data = state["func_data"]
    body_ir = func_data["body_ir"]

    key_vars_dict = dict()
    __find_key_vars(body_ir, key_vars_dict)
    loops_key_vars = [None] * (max(key_vars_dict.keys()) + 1)
    for loop_id, key_vars in key_vars_dict.items():
        loops_key_vars[loop_id] = key_vars
    func_data["loops_key_vars"] = loops_key_vars

    return {
        "func_data": func_data
    }

def __find_key_vars(items:list[IRNode], key_vars_dict:dict[int,set[str]]):
    key_vars = set()
    for item in items:
        if isinstance(item, TransNode):
            key_vars.add(item.left_var)
        if isinstance(item, TransArrNode):
            key_vars.add(item.left_arr)
        if isinstance(item, IfNode):
            for branch in item.branches:
                child_vars = __find_key_vars(branch[1], key_vars_dict)
                key_vars = key_vars.union(child_vars)
        elif isinstance(item, LoopNode):
            # print(item[-1])
            child_vars = __find_key_vars(item.body, key_vars_dict)
            child_vars = sorted(list(child_vars))
            key_vars_dict[item.loop_id]= child_vars
            key_vars = key_vars.union(child_vars)
    return key_vars