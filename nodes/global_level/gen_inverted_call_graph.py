from utils.cparser import init_tree, Node
from nodes.common import AgentState, dprint
from collections import deque
from langchain_core.messages import SystemMessage
from prompt_templates import fol_requirment_prompt

DUMMY_ROOT = None

def __traverse_tree(node:Node, call_graph:dict[str,list[str]], func_node_dict:dict[str,Node], caller:str=None):
    # 检查当前节点是否是函数定义
    if node.type == 'function_definition':
        # 找到函数声明符
        declarator = next((child for child in node.children if child.type == 'function_declarator'), None)
        if declarator:
            # 找到函数名 (identifier)
            identifier = next((child for child in declarator.children if child.type == 'identifier'), None)
            if identifier:
                caller = identifier.text.decode('utf8')
                func_node_dict[caller] = node
                # 在调用图中为这个新函数创建一个条目
                if caller not in call_graph:
                    call_graph[caller] = list()

    # 检查当前节点是否是函数调用表达式
    elif node.type == 'call_expression':
        # 调用表达式的第一个子节点通常是函数名
        function_name_node = node.children[0]
        if function_name_node.type == 'identifier':
            callee = function_name_node.text.decode('utf8')
            if callee and caller in call_graph:
                if callee not in call_graph[caller]:
                    call_graph[caller].append(callee)

    # 递归遍历所有子节点
    for child in node.children:
        __traverse_tree(child, call_graph, func_node_dict, caller)


def __invert_call_graph(call_graph: dict[str,list[str]])->dict[str,set[str]]:
    inverted_call_graph = dict()
    inverted_call_graph[DUMMY_ROOT] = set()
    for caller, callees in call_graph.items():
        if len(callees) == 0:
            inverted_call_graph[DUMMY_ROOT].add(caller)
            continue
        for callee in callees:
            if callee not in inverted_call_graph:
                inverted_call_graph[callee] = set()
            inverted_call_graph[callee].add(caller)
    return inverted_call_graph

def __extract_declared_functions(tree_root: Node) -> set[str]:
    """
    从语法树中提取所有声明的函数名（包括定义和原型声明）
    """
    declared_functions = set()

    def __traverse(node: Node):
        if node.type == 'function_declarator':
            identifier = next((child for child in node.children if child.type == 'identifier'), None)
            if identifier:
                declared_functions.add(identifier.text.decode('utf8'))

        for child in node.children:
            __traverse(child)

    __traverse(tree_root)
    return declared_functions

def gen_inverted_call_graph(state: AgentState, config) -> AgentState:
    call_graph = dict()
    func_node_dict = dict()
    code_path = config["configurable"].get("code_path")
    dprint(code_path)
    with open(code_path, "r") as f:
        code = f.read()
    tree,_ = init_tree(code)
    # 声明的函数
    declared_functions = __extract_declared_functions(tree.root_node)
    state['declared_functions'] = sorted(declared_functions)
    __traverse_tree(tree.root_node, call_graph, func_node_dict)
    inverted_call_graph = __invert_call_graph(call_graph)
    
    for func_name in inverted_call_graph.keys():
        if func_name == DUMMY_ROOT:
            continue
        if func_name not in declared_functions:
            raise Exception(f"func:'{func_name}' is not declared")

    func_to_visit_queue = deque()
    if inverted_call_graph[DUMMY_ROOT]:
        for func in inverted_call_graph[DUMMY_ROOT]:
            func_to_visit_queue.append(func)

    
    global_sys_msg = SystemMessage(content=fol_requirment_prompt)

    global_data = {
        "inverted_call_graph": inverted_call_graph,
        "func_node_dict": func_node_dict,
        "func_to_visit_queue": func_to_visit_queue,
        "fol_msg": global_sys_msg,
    }

    return {
        "global_data": global_data
    }
    #     # "messages": [global_sys_msg],
    # }