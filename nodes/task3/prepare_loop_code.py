from nodes.common import AgentState, LoopNode, conjuct_invariants
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from prompt_templates import task3_loop_code_prompt
from common import dprint, unimplement, Node, node2str


def get_current_code(func_node: Node, target_loop_id:int, loop_nodes:list[Node], func_loops_invs:list[list]):
    def is_loop_node(_node: Node) -> bool:
        return _node.type in ("for_statement", "while_statement", "do_statement")
    def __get_current_code(cur_node:Node, source_bytes, parts:list, finished=[False]):
        prev_child_end = cur_node.start_byte
        base_offset = func_node.start_byte
        if cur_node.child_count == 0:
            if cur_node.type == "comment":
                comment_text = node2str(cur_node)
                if comment_text.find("//@ assert") >= 0:
                    comment_text = comment_text.replace("//@ assert", "//@ assume")
                parts.append(comment_text)
            else:
                parts.append(node2str(cur_node))
        else:
            if is_loop_node(cur_node):
                loop_id = loop_nodes.index(cur_node)
                # 统一处理indent
                if loop_id <= target_loop_id:
                    indent = parts[-1]
                    idx = indent.rfind('\n')
                    if idx != -1:
                        indent = indent[idx+1:]
                    indent = indent
                    # 两种情况
                    loop_name = f"LOOP_{loop_id}"
                    if loop_id < target_loop_id:
                        inv = conjuct_invariants(func_loops_invs[loop_id])
                        # 使注释在循环上面一行
                        parts.append(f"//@ {loop_name} invariant: {inv}\n")
                        parts.append(indent)
                        # 给循环添加label
                        parts.append(f"{loop_name}:")
                    elif loop_id == target_loop_id:
                        # 给循环添加label
                        # parts.append(f"TARGET_LOOP:")
                        parts.append(f"{loop_name}:")
            for i, child in enumerate(cur_node.children):
                # 当前结点和前面结点之间的换行和缩进
                indent:str = source_bytes[prev_child_end-base_offset:child.start_byte-base_offset].decode('utf8')
                parts.append(indent)
                if finished[0]:
                    # 在target_loop的父节点，处理它之后紧挨着的assert注释
                    if child.type == "comment" and i > 0:
                        pre_node = cur_node.children[i-1]
                        if is_loop_node(pre_node) and loop_nodes.index(pre_node) == target_loop_id:
                            parts.append(node2str(child))
                    break 
                __get_current_code(child, source_bytes, parts, finished)
                prev_child_end = child.end_byte
            # 防止直接把后面本该截取的代码部分也添加进parts
            if not finished[0]:
                # 最后一个结点和前面结点之间的换行和缩进
                parts.append(source_bytes[prev_child_end-base_offset:cur_node.end_byte-base_offset].decode('utf8'))
            if is_loop_node(cur_node): 
                loop_id = loop_nodes.index(cur_node)
                if loop_id == target_loop_id:
                    finished[0] = True
                
    parts = []
    __get_current_code(func_node, func_node.text, parts)
    code = ''.join(parts)
    return code

def prepare_loop_code(state: AgentState, config) -> AgentState:
    llm = config["configurable"].get("llm")
    global_data = state["global_data"]
    func_data = state["func_data"]
    loop_data = state["loop_data"]
    task3_data = state["task3_data"]
    key_vars = loop_data["key_vars"]

    func_node = global_data["func_node_dict"][func_data["cur_name"]]
    func_loops_invs = func_data["loops_invs"]
    loop_nodes = func_data["loop_nodes"]
    loop_ir_node:LoopNode = loop_data["path_to_loop"][-1]

    # 构建code_msg
    true_func_code = get_current_code(
        func_node,
        loop_ir_node.loop_id, 
        loop_nodes, 
        func_loops_invs
    )
    loop_name = f"LOOP_{loop_ir_node.loop_id}"
    prompt = task3_loop_code_prompt.format(
        func_code=true_func_code,
        loop_name=loop_name,
        loop_key_vars=",".join([f"`{key_var}`" for key_var in key_vars]),
    )
    loop_sys_msg_post = SystemMessage(content=prompt)