from ast import expr, pattern
import re
from nodes.common import AgentState, get_vars_from_str
from common import node2str, unimplement, dprint
from collections import deque
from utils.cparser import Node

from common import (
    # TY_RET,
    # TY_TRANS_POINTER,
    # # TY_TRANS_ARR,
    # TY_DECLARE,
    VAR_POINTER, 
    VAR_ARRAY,
)


from nodes.common import (
    AssumeNode,
    IfNode,
    IfCondNode,
    TransNode,
    LoopNode,
    AssertNode,
    TransArrNode,
    DeclareNode,
    FuncParamDeclareNode
)

loop_counter:int


# 'a[a[i]]' -> {'a[i]', 'i'}
def extract_bracket_contents(s):
    result = set()
    stack = []
    for i, char in enumerate(s):
        if char == '[':
            stack.append(i)
        elif char == ']':
            if stack:
                start = stack.pop()
                content = s[start+1:i]
                result.add(content.strip())
    
    return result

def parse_func(state: AgentState)->AgentState:
    func_data = state["func_data"]
    func_node = func_data["cur_node"]
    loop_nodes = list()
    global loop_counter
    loop_counter = 0
    var_type_dict, body_ir, ret_type = __parse_func(func_node, loop_nodes)

    func_data["var_type_dict"] = var_type_dict
    func_data["body_ir"] = body_ir
    func_data["ret_type"] = ret_type
    func_data["loop_nodes"] = loop_nodes

    return {
        "func_data": func_data,
    }


def __handle_declaration(node:Node, var_dict:dict)->list[tuple[str,str]]:
    transforms = []
    type_node = node.child_by_field_name("type")
    # 处理基本数据类型
    # if type_node.type == "primitive_type":
    if type_node.type in ["primitive_type","sized_type_specifier"]:
        var_type = node2str(type_node)
        if var_type == "unsigned int":
            var_type = "int"
        for declarator in node.children_by_field_name("declarator"):
            # example: int i;
            if declarator.type == "identifier":
                var_name = node2str(declarator)
                var_dict[var_name] = (var_type,)
                transforms.append(DeclareNode(var_name))
            elif declarator.type == "pointer_declarator":
                pointer_name_node = declarator.child_by_field_name("declarator")
                pointer_name = node2str(pointer_name_node)
                transforms.append(DeclareNode(pointer_name))
                var_dict[pointer_name] = (VAR_POINTER, (var_type, ))
            # notice here!!!!!!
            elif declarator.type == "array_declarator":
                pointer_name_node = declarator.child_by_field_name("declarator")
                pointer_name = node2str(pointer_name_node)
                transforms.append(DeclareNode(pointer_name))
                var_dict[pointer_name] = (VAR_POINTER, (var_type, ))
            # example:
            # int i = 0;
            # int a[2] = {1,2};
            elif declarator.type == "init_declarator":
                var_name_node = declarator.child_by_field_name("declarator")
                if var_name_node.type == "identifier":
                    var_name = node2str(var_name_node)
                    value_node = declarator.child_by_field_name("value")
                    expr = node2str(value_node)
                    var_dict[var_name] = (var_type,)
                    transforms.append(DeclareNode(var_name))
                    transforms.append(TransNode(var_name, expr))
                elif var_name_node.type == "array_declarator":
                    # 保存定义
                    arr_name_node = var_name_node.child_by_field_name("declarator")
                    arr_size_node = var_name_node.child_by_field_name("size")
                    arr_name = node2str(arr_name_node)
                    arr_size = int(node2str(arr_size_node))
                    var_dict[arr_name] = (VAR_ARRAY, (var_type, ), arr_size)
                    transforms.append(DeclareNode(arr_name))
                    # 保存数组内容
                    values_node = declarator.child_by_field_name("value")
                    for idx, val_node in enumerate(values_node.named_children):
                        transforms.append((TY_TRANS_POINTER, arr_name, node2str(val_node), idx))
                elif var_name_node.type == "pointer_declarator":
                    pointer_name_node = var_name_node.child_by_field_name("declarator")
                    pointer_name = node2str(pointer_name_node)
                    value_node = declarator.child_by_field_name("value")
                    expr = node2str(value_node)
                    var_dict[pointer_name] = (VAR_POINTER, (var_type, ))
                    transforms.append((TY_TRANS_POINTER, pointer_name, expr))
                else:
                    unimplement(f"{var_name_node.type}")
            # example: int func();
            # elif declarator.type == "function_declarator":
            #     func_name_node = declarator.child_by_field_name("declarator")
            #     func_name = node2str(func_name_node)
            #     func_dict[func_name] = var_type
            else:
                unimplement()
    else:
        unimplement()
    return transforms

def __handle_expression(node:Node, handle_child=True)->list[tuple[str,str]]:
    def __inner_handle_expression(node:Node)->list[tuple[str,str]]:
        __transforms = []
        if node.type == "comma_expression":
            __transforms.extend(__inner_handle_expression(node.child_by_field_name("left")))
            __transforms.extend(__inner_handle_expression(node.child_by_field_name("right")))
        elif node.type == "parenthesized_expression":
            inner = node.named_children[0]
            __transforms.extend(__inner_handle_expression(inner))
        else:
            # 很tricky的在这里处理assume索引为非负整数
            arr_indexes = extract_bracket_contents(node2str(node))
            for arr_index in arr_indexes:
                 __transforms.append(AssumeNode(f"{arr_index}>=0"))
            
            if node.type == "assignment_expression":
                right_node = node.child_by_field_name("right")
                right_expr = node2str(right_node)
                left_node = node.child_by_field_name("left")
                operator_node = node.child_by_field_name("operator")
                operator = node2str(operator_node)
                if left_node.type == "identifier":
                    var_name = node2str(left_node)
                    # 处理 x += 1的情况
                    if operator != "=":
                        right_expr = var_name + operator[:-1] + right_expr
                    __transforms.append(TransNode(var_name, right_expr))
                elif left_node.type == "subscript_expression":
                    argument_node = left_node.child_by_field_name("argument")
                    index_node = left_node.child_by_field_name("index")
                    if argument_node and index_node:
                        arr_name = node2str(argument_node)
                        index = node2str(index_node)
                        __transforms.append(TransArrNode(arr_name, index, right_expr))
                    else:
                        unimplement("subscript_expression")
                elif left_node.type == "pointer_expression":
                    pointer_name_node = left_node.child_by_field_name("argument")
                    pointer_name = node2str(pointer_name_node)
                    __transforms.append((TY_TRANS_DEPOINTER, pointer_name, right_expr))
                else:
                    unimplement("")
            elif node.type == "call_expression":
                unimplement("")
            elif node.type == "update_expression":
                var_name_node = node.child_by_field_name("argument")
                operator_node = node.child_by_field_name("operator")
                var_name = node2str(var_name_node)
                operator = node2str(operator_node)
                if operator == "++":
                    __transforms.append(TransNode(var_name,f"{var_name}+1"))
                elif operator == "--":
                    __transforms.append(TransNode(var_name, f"{var_name}-1"))
                else:
                    unimplement()
            else:
                unimplement(node.type)
        return __transforms
    if handle_child:
        assert node.named_child_count == 1
        target_node = node.named_children[0]
    else:
        target_node = node
    return __inner_handle_expression(target_node)


# ("if",[(cond,transforms)])
def __handle_if(root_node:Node, var_dict, loop_nodes, pre_depth)->tuple[str,list[tuple[str,list]]]:
    def handle_body(body_node:Node)->list:
        if body_node.type == "expression_statement":
            return __handle_expression(body_node)
        elif body_node.type == "compound_statement":
            return __handle_block(body_node, var_dict, loop_nodes, pre_depth+1)
    cur_if_node = root_node
    pre_conds = []
    else_body = None
    if_branch = []

    # 只处理 if 和 elif
    while cur_if_node:
        cond_node = cur_if_node.child_by_field_name("condition")
        next_node = None
        cond_expr = node2str(cond_node)[1:-1]
        pre_conds.append(f"({cond_expr})")
        body_node = cur_if_node.child_by_field_name("consequence")
        elif_node = cur_if_node.child_by_field_name("alternative")
        if elif_node is None:
            next_node = None
        else:
            next_node = elif_node.named_children[0]
            if next_node.type in ["compound_statement", "expression_statement"]:
                else_body = next_node
                next_node = None
        cur_if_node = next_node
        inner = handle_body(body_node)
        if_branch.append((cond_expr, inner))
    # 不管是否有显式的else，都要处理
    pre_conds = "||".join(pre_conds)
    cond_expr = f"!({pre_conds})"
    if else_body:
        inner = handle_body(else_body)
    else:
        inner = []
    if_branch.append((cond_expr, inner))
    return IfNode(if_branch)

def __handle_return(ret_node:Node):
    ret_var_node = ret_node.named_children[0]
    res = None
    if ret_var_node.type == "identifier":
        ret_var = node2str(ret_var_node)
        res = (TY_RET, ret_var)
    else:
        unimplement()
    
    return res


def add_to_var_deps(var_deps:dict[str, set[str]], left_var:str, right_var:str):
    if left_var not in var_deps:
        var_deps[left_var] = set()
    var_deps[left_var].add(right_var)

def handle_var_deps_for_loop(var_deps:dict[str, set[str]], guard:str):
    guard_vars = get_vars_from_str(guard)
    for guard_var in guard_vars:
        for var in var_deps:
            add_to_var_deps(var_deps, var, guard_var)

def merge_var_deps(var_deps1:dict[str, set[str]], var_deps2:dict[str, set[str]]):
    result = {}
    for key, value_set in var_deps1.items():
        result[key] = value_set.copy()
    for key, value_set in var_deps2.items():
        if key in result:
            result[key].update(value_set)
        else:
            result[key] = value_set.copy()
    return result

        
def get_var_deps(nodes:list):
    var_deps:dict[str, set[str]] = dict()
    for node in nodes:
        if isinstance(node, TransNode):
            right_vars = get_vars_from_str(node.right_val)
            left_var = node.left_var
            for var in right_vars:
                add_to_var_deps(var_deps, left_var, var)
        elif isinstance(node, TransArrNode):
            right_vars = get_vars_from_str(node.right_val)
            left_var = node.left_arr
            for var in right_vars:
                add_to_var_deps(var_deps, left_var, var)
        elif isinstance(node, IfNode):
            for branch in node.branches:
                cond = branch[0]
                body = branch[1]
                cond_vars = get_vars_from_str(cond)
                sub_var_deps = get_var_deps(body)
                var_deps = merge_var_deps(var_deps, sub_var_deps)
                # 这个if里的key_vars都依赖于cond_vars
                for var in cond_vars:
                    for sub_var in sub_var_deps:
                        add_to_var_deps(var_deps, sub_var, var)
        elif isinstance(node, LoopNode):
            sub_var_deps = get_var_deps(node.body)
            var_deps = merge_var_deps(var_deps, sub_var_deps)
            guard_vars = get_vars_from_str(node.guard)
            # 这个for里的key_vars都依赖于cond_vars
            for var in guard_vars:
                for sub_var in sub_var_deps:
                    add_to_var_deps(var_deps, sub_var, var)
        
        else:
            pass
            # unimplement()
    return var_deps



def __handle_loop(loop_node:Node, var_dict, loop_nodes:list[Node], pre_depth):
    transforms = []
    cond_node = loop_node.child_by_field_name("condition")
    cond_expr = node2str(cond_node)
    body_node = loop_node.child_by_field_name("body")
    body_trans = __handle_block(body_node, var_dict, loop_nodes, pre_depth+1)
    
    transforms.extend(body_trans)
    if loop_node.type == "for_statement":
        # update块
        update_node = loop_node.child_by_field_name("update")
        post_update_trans = __handle_expression(update_node,handle_child=False)
        transforms.extend(post_update_trans)
    global loop_counter
    old_counter = loop_counter
    loop_nodes.append(loop_node)
    loop_counter += 1

    post_assert = None

    var_deps = get_var_deps( transforms )

    # 然后再对loop_guard做处理
    handle_var_deps_for_loop(var_deps, cond_expr)

    return LoopNode(
        cond_expr,
        transforms,
        pre_depth,
        old_counter, 
        post_assert,
        var_deps
    )

def __extract_balanced_parentheses_content(s, prefix):
    start = s.find(prefix)
    if start == -1:
        return None
    # 找第一个 '(' 的位置
    pos = s.find('(', start)
    if pos == -1:
        return None

    count = 1
    i = pos + 1
    while i < len(s):
        if s[i] == '(':
            count += 1
        elif s[i] == ')':
            count -= 1
            if count == 0:
                # 找到匹配的右括号，返回内容（中间不含外层括号）
                return s[pos + 1:i]
        i += 1
    return None

def __handle_comment(node: Node):
    s = node2str(node)

    content = __extract_balanced_parentheses_content(s, '//@ assume')
    if content is not None:
        content = content.strip()
        # 去掉尾部多余的分号
        if content.endswith(';'):
            content = content[:-1].rstrip()
        return [AssumeNode(content)]

    content = __extract_balanced_parentheses_content(s, '//@ assert')
    if content is not None:
        content = content.strip()
        if content.endswith(';'):
            content = content[:-1].rstrip()
        return [AssertNode(content)]

    return []


def __handle_block(root_node:Node, var_dict:dict, loop_nodes, cur_depth)->list:
    scope_data = []
    for idx, node in enumerate(root_node.named_children):
        if node.type == "comment":
            res = __handle_comment(node)
            if len(res) > 0:
                dprint(res)
            # 把assert放到上一个且相邻loop中
            # 即每个循环后只允许一个assert
            if len(res)>0 and isinstance(res[0],AssertNode):
                last_loop_item = scope_data[-1]
                assert( isinstance(last_loop_item,LoopNode) )
                last_loop_item.post_condition = res[0].expr
                scope_data[-1] = last_loop_item
            else:
                scope_data.extend(res)
        elif node.type == "declaration":
            res = __handle_declaration(node, var_dict)
            scope_data.extend(res)
        elif node.type == "expression_statement":
            res = __handle_expression(node)
            scope_data.extend(res)
        elif node.type == "compound_statement":
            res = __handle_block(node, var_dict, loop_nodes, cur_depth+1)
            scope_data.extend(res)
        elif node.type == "if_statement":
            res = __handle_if(node, var_dict, loop_nodes, cur_depth)
            scope_data.append(res)
        elif node.type == "return_statement":
            pass
            # scope_data.append(__handle_return(node))
        elif node.type in ["while_statement", "for_statement"]:
            if node.type == "for_statement":
                # initializer块
                initializer = node.child_by_field_name("initializer")
                if initializer:
                    if initializer.type == "declaration":
                        scope_data.extend(__handle_declaration(initializer, var_dict))
                    elif initializer.type in ["assignment_expression", "comma_expression"]:
                        scope_data.extend(__handle_expression(initializer, handle_child=False))
                    else:
                        unimplement()
            res = __handle_loop(node, var_dict, loop_nodes, cur_depth)
            scope_data.append(res)
        elif node.type not in ["do_statement"]:
            unimplement(node.type)
    return scope_data

# def list_to_generator(data:list, cond_func):
#     for item in data:
#         ty = item[0]
#         if ty not in [TY_IF, TY_LOOP]:
#             yield item
#         if ty == TY_IF:
#             for branch in item[1]:
#                 cond = branch[0]
#                 body = branch[1]
#                 cond_func(0, cond)
#                 yield from list_to_generator(body, cond_func)
#                 cond_func(1)
#         if ty == TY_LOOP:
#             yield True

def __parse_func(func_node: Node, loop_nodes):
    # 函数签名
    ret_type = node2str(func_node.child_by_field_name("type"))
    func_declarator = func_node.child_by_field_name("declarator")
    if func_declarator.type == "pointer_declarator":
        ret_type += "*"
        true_declarator = func_declarator.child_by_field_name("declarator")
    else:
        true_declarator = func_declarator
    param_list_node = true_declarator.child_by_field_name("parameters")
    var_dict = dict()

    param_declare_nodes:list[DeclareNode] = []
    for param_node in param_list_node.named_children:
        param_declare_nodes.extend(__handle_declaration(param_node, var_dict))
    tmp_nodes = []
    for node in param_declare_nodes:
        tmp_nodes.append(FuncParamDeclareNode(node.var_name))
    param_declare_nodes = tmp_nodes
    # 函数体
    body_node = func_node.child_by_field_name("body")
    if body_node is None:
        unimplement("函数无体")
    body_info = __handle_block(body_node, var_dict, loop_nodes, 0)

    body_info = param_declare_nodes + body_info
    # dprint(body_info)

    return (var_dict, body_info, ret_type)