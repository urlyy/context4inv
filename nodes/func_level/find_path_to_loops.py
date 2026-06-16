from common import (
    # TY_IF, TY_LOOP, 
    # TY_IF_COND,
    dprint
)
from nodes.common import (
    AgentState, LoopNode, IfNode, IfCondNode, OuterLoopGuardNode
)

def modify_var_deps(node:LoopNode):
    def stop(name):
        return name.startswith("unknown")
    
    new_var_deps = dict()
    for var, deps in node.var_deps.items():
        if stop(var):
            continue
        tmp_set = set()
        for dep in deps:
            if stop(dep):
                continue
            if var == dep:
                continue
            tmp_set.add(dep)
        if len(tmp_set) == 0:
            continue
        new_var_deps[var] = tmp_set
        

    node.var_deps = new_var_deps

def __traverse(data:list):
    paths = []

    def __inner_traverse(items:list, prefix_path:list):
        current_depth_block = []
        for item in items:
            if isinstance(item, LoopNode):
                cond, body = item.guard, item.body
                paths.append(prefix_path+current_depth_block+[item])
                loop_id = item.loop_id
                # dprint(item.var_deps)
                modify_var_deps(item)
                # dprint(item.var_deps)
                __inner_traverse(body, prefix_path+current_depth_block+[OuterLoopGuardNode(cond, loop_id)])
            elif isinstance(item, IfNode):
                # 遍历'if'语句的每一个分支
                for cond, body in item.branches:
                    __inner_traverse(body, prefix_path+current_depth_block+[IfCondNode(cond)])
            current_depth_block.append(item)

    __inner_traverse(data, [])
    paths.sort(key=lambda p: ( p[-1].loop_id ))
    return paths
    
def find_path_to_loops(state:AgentState)->AgentState:
    func_data = state["func_data"]
    body_ir = func_data["body_ir"]

    paths = __traverse(body_ir)
   
    # for path in paths:
    #     dprint(path)

    func_data["path_to_loops"] = paths

    # for path in paths:
    #     node: LoopNode = path[-1]
    #     dprint(node.guard)
    #     dprint(node.var_deps)

    # 因为修改了var_deps
    func_data["body_ir"] = body_ir

    # exit()

    return {
        "func_data": func_data
    }