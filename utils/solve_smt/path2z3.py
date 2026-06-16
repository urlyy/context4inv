'''
当前仅支持：
整型+浮点型和数值运算

不支持do-while
不支持字符串
不支持switch
不支持指针
不支持外部函数内部细节
不支持数组
不支持常量分析

不支持常量折叠和表达式简化

condition里的赋值语句可能处理不好

unknown没有处理
可以使用 solver() 方法将策略转换为 solver 对象。 如果策略产生空目标，则关联的求解器返回 sat。 如果策略生成包含 False 的单个目标，则求解器返回 unsat。 否则，它将返回 unknown。
'''

import subprocess
import sys
import re
from utils.cparser import init_tree,  Node,  Tree, Language
from utils.format_py import format_py
import json
from utils import expr_parser
from utils.fol_parser import fol_to_z3, replace_old
import copy
import ast


from string import Template

from common import (
    # TY_IF, TY_LOOP, TY_IF_COND, TY_ASSUME, TY_ASSERT,TY_TRANSFORM,
    # TY_RET, TY_TRANS_POINTER,
    dprint,
    VAR_ARRAY, TAB, 
    VAR_POINTER, 
)

from nodes.common import (
    LoopNode, IRNode, IfNode, IfCondNode, 
    TransNode, AssumeNode, AssertNode,
    TransArrNode, OuterLoopGuardNode, DeclareNode, FuncParamDeclareNode
)

import sys

Z3_CODE_TEMPLATE  = Template("""from z3 import *
import json
import sys

__output_counterexample_file = None     
if len(sys.argv) == 2:
    __output_counterexample_file = sys.argv[1]

__solver = Solver()

# 声明符号变量
$DECLARE
# 声明不变式中量词的bind                        
{}
# 循环不变式
def INV($INV_PARAMS):
    # {}
    return {}
# 循环前的初始化代码
PRE=$PRE
# 循环条件
G=$G
# 循环体内的变量更新
TRANS=$TRANS
$POST_CODE

def check(solver:Solver, step:int):
    res = solver.check()
    if res == sat:
        if step == 0:
            print("[失败] 循环前置条件不成立！模型如下：")
        elif step == 1:
            print("[失败] 循环不变式不保持！模型如下：")
        elif step == 2:
            print("[失败] 循环后置条件不成立！模型如下：")
        model = solver.model()
        counterexample = dict()
        $SAVE_COUNTEREXAMPLE
        print(counterexample)
        if __output_counterexample_file:
            result = dict()
            result["reason"] = step
            result["counterexample"] = counterexample
            res_str = json.dumps(result)
            with open(__output_counterexample_file, "w") as f:
                f.write(res_str)
        # 必须异常返回码
        exit(13)
    elif res == unknown:
        if __output_counterexample_file:
            result = dict()
            result["reason"] = step
            result["unknown_reason"] = solver.reason_unknown()
            res_str = json.dumps(result)
            with open(__output_counterexample_file, "w") as f:
                f.write(res_str)
        exit(14)
                             

$EVALUATE

print("循环不变式成立")
""")

def unimplement(log:str=""):
    raise Exception(f"unimplement: {log}")

def node2str(node:Node, remove_space=True):
    txt = node.text.decode("utf-8")
    if remove_space:
        txt = txt.replace(" ", "")
    return txt

def get_z3_type(c_type:tuple)->str:
    type_name = c_type[0]
    if type_name in ["int", "long"]:
        return "Int"
    elif type_name in ["float", "double"]:
        return "Real"
    elif type_name == VAR_POINTER:
        return VAR_POINTER
    else:
        unimplement(f"暂未实现的类型: {c_type}")

def get_ssa_var_name(var_name, cur_idx)->str:
    return f"{var_name}_{cur_idx}"

def transform_right_expr(expr:str, var_type_dict, cur_var_counter:dict)->str:
    res_expr = expr
    # 变量名替换
    for name in var_type_dict.keys():
        assert name in cur_var_counter
        if re.search(rf"\b{name}\b", res_expr):
            # 先替换
            true_name = get_ssa_var_name(name, cur_var_counter[name])
            res_expr = re.sub(rf"\b{name}\b", true_name, res_expr)
            # 还要为依赖图做准备
    # 函数替换
    # for name in func_dict.keys():
    #     func_pattern = rf'\b{name}\(.*?\)'
    #     # 替换为函数名本身
    #     while re.search(func_pattern, res_expr):
    #         call_func_idx = call_counter[func_name]
    #         true_name = get_ssa_var_name(name, call_func_idx+1)
    #         res_expr = re.sub(func_pattern, true_name, res_expr, count=1)
    #         call_counter[func_name]  = call_func_idx + 1
    #     # res_expr = re.sub(func_pattern, name, res_expr)
    res = expr_parser.handle_expr(res_expr)
    return res

def transform_ssa_inv(inv:str, var_type_dict:dict, cur_var_counter:dict):
    res_inv = inv
    # 先获得quantifier变量
    _, quantifier_binder_var_set = fol_to_z3(res_inv)
    unexist_uantifier_binder_var_set = set()
    if len(quantifier_binder_var_set)>0:
        for binder_var in quantifier_binder_var_set:
            if var_type_dict.get(binder_var) is None:
                unexist_uantifier_binder_var_set.add(binder_var)
                var_type_dict[binder_var] = ("int",)
                cur_var_counter[binder_var] = 0
    # 变量名替换
    tmp_inv = inv
    for name in var_type_dict.keys():
        assert name in cur_var_counter
        if re.search(rf"\b{name}\b", tmp_inv):
            # 先替换
            true_name = get_ssa_var_name(name, cur_var_counter[name])
            tmp_inv = re.sub(rf"\b{name}\b", true_name, tmp_inv)
    z3_s, _ = fol_to_z3(tmp_inv)

    # for name in var_type_dict.keys():
    #     assert name in cur_var_counter
    #     if re.search(rf"\b{name}\b", res_inv):
    #         # 先替换
    #         true_name = get_ssa_var_name(name, cur_var_counter[name])
    #         res_inv = re.sub(rf"\b{name}\b", true_name, res_inv)
    # z3_s, _ = fol_to_z3(res_inv)

    # # if len(quantifier_binder_var_set) > 3:
    # #     dprint("qwerqwerqwer")
    # #     dprint(quantifier_binder_var_set)
    # #     exit()
    # dprint(z3_s)
    # dprint(quantifier_binder_var_set)

    return z3_s, unexist_uantifier_binder_var_set


def handle_stringfy_items(items:list[tuple["str",any]], var_type_dict, cur_var_counter:dict, old_var_counter:dict, declared_vars:set[str], loops_invs:list[set[str]], loops_key_vars:list[list[str]], depth=0, solver_add=True)->str:
    s = ""
    all_quantifier_binder_var_set = set()
    new_var_counter = copy.deepcopy(old_var_counter)
    for item in items:
        tmp_s = ""
        
        # if item[0] not in [TY_TRANSFORM, TY_IF, TY_IF_COND, TY_LOOP, TY_ASSUME]:
        #     unimplement(item)
        if isinstance(item, DeclareNode):
            declared_vars.add(item.var_name)
            continue
        elif isinstance(item, LoopNode):
            # 替换为循环不变式
            # 已得到不变式的循环
            loop_idx = item.loop_id
            loop_invs:set = loops_invs[loop_idx]
            # use entrance var to replace old
            loops_replaced_old = set()
            for inv in loop_invs:
                loops_replaced_old.add(replace_old(inv, cur_var_counter, declared_vars))
            # 注意这里要带上内层循环的退出条件
            loop_invs = list(loops_replaced_old) + [f"!({item.guard})"]
            # this loop's key_var_idx++
            for key_var in loops_key_vars[loop_idx]:
                cur_var_counter[key_var] += 1
            
            z3_invs = []
            for inv in loop_invs:
                try:
                    z3_s, quantifier_binder_var_set = transform_ssa_inv(inv, var_type_dict, cur_var_counter)
                except Exception as e:
                    e.args = f"{e.args[0]} at path2z3"
                    raise
                # for binder_var in quantifier_binder_var_set:
                #     all_quantifier_binder_var_set.add(binder_var)
                z3_invs.append(f"{TAB * depth }{z3_s}")
            tmp_s = f"And({','.join(z3_invs)})"
        elif isinstance(item, OuterLoopGuardNode):
            # enter a outer loop, make its key_var_idx++
            this_loop_key_vars = loops_key_vars[item.loop_id]
            new_var_counter = copy.deepcopy(cur_var_counter)
            old_entry_counter = copy.deepcopy(cur_var_counter)
            for var in this_loop_key_vars:
                cur_var_counter[var] += 1
            # then assume guard
            cond_s = transform_right_expr(item.expr, var_type_dict, cur_var_counter)
            tmp_s += f"{TAB * depth }{cond_s}"
            # if outer loop invariants are known, add them to constrain bumped key_vars
            # (Hoare logic: at loop body entry, invariant /\ guard holds)
            if item.loop_id < len(loops_invs) and loops_invs[item.loop_id]:
                outer_invs = loops_invs[item.loop_id]
                for outer_inv in outer_invs:
                    outer_inv_replaced = replace_old(outer_inv, old_entry_counter, declared_vars)
                    try:
                        z3_s, _ = transform_ssa_inv(outer_inv_replaced, var_type_dict, cur_var_counter)
                        tmp_s += f",\n{TAB * depth }{z3_s}"
                    except Exception:
                        pass
        elif isinstance(item, TransNode):
            var_name, right_expr = item.left_var, item.right_val
            right_s = transform_right_expr(right_expr, var_type_dict, cur_var_counter)
            ssa_idx = cur_var_counter[var_name]
            cur_var_counter[var_name] = ssa_idx + 1
            ssa_new_name = get_ssa_var_name(var_name, ssa_idx + 1)
            tmp_s += f"{TAB * depth }{ssa_new_name}=={right_s}"
        elif isinstance(item, IfCondNode):
            cond_s = transform_right_expr(item.expr, var_type_dict, cur_var_counter)
            tmp_s += f"{TAB * depth }{cond_s}"
        elif isinstance(item, TransArrNode):
            arr_name = item.left_arr
            right_s = transform_right_expr(item.right_val, var_type_dict, cur_var_counter)
            ssa_idx = cur_var_counter[item.left_arr]
            ssa_old_name = get_ssa_var_name(arr_name, ssa_idx)
            cur_var_counter[arr_name] = ssa_idx + 1
            arr_idx = transform_right_expr(item.index, var_type_dict, cur_var_counter)
            ssa_new_name = get_ssa_var_name(arr_name, ssa_idx + 1)
            tmp_s += f"{TAB * depth}{ssa_new_name}==Store({ssa_old_name}, {arr_idx}, {right_s})"
        # elif item[0] == TY_TRANS_POINTER:
        #     pointer_name, right_expr = item[1:3]
        elif isinstance(item, IfNode):
            # [(cond, sub_str, end_var_counter)]
            branches = []
            for cond,body in item.branches:
                # 每个if都是同一个counter起点
                tmp_var_counter = dict(cur_var_counter)
                cond = transform_right_expr(cond, var_type_dict, cur_var_counter)
                sub_str, sub_quantifier_binder_var_set = handle_stringfy_items(body, var_type_dict, tmp_var_counter, new_var_counter, declared_vars, loops_invs, loops_key_vars, depth+1, solver_add)
                # print(tmp_var_counter)
                # for binder_var in sub_quantifier_binder_var_set:
                #     all_quantifier_binder_var_set.add(binder_var)
                branches.append((cond, sub_str, tmp_var_counter))
            # 合并counter
            for _,_,end_var_counter in branches:
                # print(end_var_counter)
                for k,v in end_var_counter.items():
                    cur_var_counter[k] = max(cur_var_counter[k], v)
            # 然后要统一if里的结束时的统一变量的下标
            branch_strs = []
            for cond,sub_str,end_var_counter in branches:
                for k,v in end_var_counter.items():
                    expect_idx = cur_var_counter[k]
                    if v != expect_idx:
                        left_var = get_ssa_var_name(k, expect_idx)
                        right_var = get_ssa_var_name(k, v)
                        sub_str += f"{left_var}=={right_var},\n"
                branch_strs.append(f"And({cond},And(\n{sub_str})\n),")
            tmp_s += "Or(\n" +  "\n".join(branch_strs) + "\n)"
        elif isinstance(item, AssumeNode):
            inv = item.expr
            # assume don't support old
            # inv = replace_old(inv, cur_var_counter, declared_vars)
            z3_s, quantifier_binder_var_set = transform_ssa_inv(inv, var_type_dict, cur_var_counter)
            # for binder_var in quantifier_binder_var_set:
            #     all_quantifier_binder_var_set.add(binder_var)
            tmp_s += f"{TAB * depth }{z3_s}"
        else:
            unimplement(item)
        
        s += f"{TAB * depth }"
        # if solver_add and depth == 0:
        #     s += f"__solver.add({tmp_s})\n"
        # else:
        s += f"{tmp_s},\n"
    return s, all_quantifier_binder_var_set

def get_declare_code(var_type_dict, var_counter):
    declare_code = ""
    for name, typ in var_type_dict.items():
        counter = var_counter[name]
        z3_type = get_z3_type(typ)
        if z3_type != VAR_POINTER:
            true_names = [get_ssa_var_name(name, idx) for idx in range(0, counter + 1)]
            left_names = ','.join(true_names)
            if len(true_names) == 1:
                left_names += ","
            declare_code += f"{left_names}={z3_type}s('{' '.join(true_names)}')\n"
        else:
            item_type = get_z3_type(typ[1])
            for idx in range(0, counter + 1):
                ssa_var_name = get_ssa_var_name(name, idx)
                declare_code += f"{ssa_var_name}=Array('{ssa_var_name}', IntSort(), {item_type}Sort())\n"
    return declare_code
    
def get_save_counterexample_code(var_type_dict, var_counter):
    vars = []
    for var_name in var_type_dict.keys():
        cnt = var_counter[var_name]
        for i in range(0, cnt+1):
            vars.append(get_ssa_var_name(var_name, i))
    save_counterexample_s = f'''z3_vars = [{','.join(vars)}]
        for z3_var in z3_vars:
            counterexample[str(z3_var)] = str(model.eval(z3_var, True))
'''
    return save_counterexample_s



def first_comparison_sign(expr: str, key_vars: set):
    expr = expr.replace("&&", "and").replace("||", "or")
    op_map = {
        ast.Lt: "<",
        ast.LtE: "<=",
        ast.Gt: ">",
        ast.GtE: ">=",
        ast.Eq: "==",
        ast.NotEq: "!="
    }

    class Visitor(ast.NodeVisitor):
        def __init__(self):
            self.result = None  # (key_var, sign)

        def visit_Compare(self, node):
            if self.result is not None:
                return  # 已找到第一个

            # 提取运算符
            ops = [op_map[type(op)] for op in node.ops if type(op) in op_map]

            # 提取涉及关键变量
            vars_in_node = [n.id for n in ast.walk(node) if isinstance(n, ast.Name) and n.id in key_vars]

            if vars_in_node:
                if len(ops) != 1:
                    return  # 链式比较暂不支持，直接跳过
                
                op = ops[0]
                sign = -1 if op in ("<", "<=") else 1 if op in (">", ">=") else None
                if sign is None:
                    return  # 不支持的比较运算符，直接返回 None

                # 只取第一个关键变量
                self.result = (vars_in_node[0], sign)

            self.generic_visit(node)

    tree = ast.parse(expr, mode="eval")
    visitor = Visitor()
    visitor.visit(tree)

    return visitor.result

def __path2z3(path_to_loop:list, key_vars:list[str], var_type_dict:dict, loops_invs:list[set[str]], loops_key_vars:list[list[str]], func_spec_dict:dict, pre_task_template_path, post_task_template_path)->tuple:
    # 最终返回的
    ssa_dict_after_pre = dict()
    ssa_dict_before_loop = dict()
    ssa_dict_after_trans = dict()
    ssa_dict_after_loop = dict()

    # 开始操作
    # example: {"x":3, "y":4}, so x => x_3
    var_counter = dict()
    for var_name in var_type_dict.keys():
        var_counter[var_name] = 0
    declared_vars = set()

    old_var_counter = dict()
    

    # call_counter = dict()
    # for func_name in func_dict.keys():
    #     call_counter[func_name] = 0


    # 严格按照下列顺序处理
    # 1. 处理初始化阶段的状态转移
    pre_ir = path_to_loop[:-1]
    # print(pre_ir)

    # firstly collect func_param
    idx = 0
    for node in pre_ir:
        if isinstance(node, FuncParamDeclareNode):
            old_var_counter[node.var_name] =  0
            declared_vars.add(node.var_name)
        else:
            break
        idx+=1
    
    pre_ir = pre_ir[idx:]
    pre_code, quantifier_binder_var_set = handle_stringfy_items(pre_ir, var_type_dict, var_counter, old_var_counter, declared_vars, loops_invs, loops_key_vars)
    # for binder_var in quantifier_binder_var_set:
    #     if binder_var not in var_type_dict:
    #         var_type_dict[binder_var] = ("int",)
    #         var_counter[binder_var] = 0
    # print(pre_code)
    # print(var_counter)
    

    # 2. 保存初始化后的变量ssa状态
    key_vars_after_pre = set()
    for key_var in key_vars:
        key_vars_after_pre.add(get_ssa_var_name(key_var, var_counter[key_var]))
    for var_name in var_counter:
        ssa_dict_after_pre[var_name] = get_ssa_var_name(var_name, var_counter[var_name])

    
    # 3. 初始化后状态的关键变量的计数器ssa+1，转移到循环前状态
    # because enter a loop(though target), key_var_idx++
    for var in var_type_dict:
        if var in key_vars:
            var_counter[var] += 1

    key_vars_before_loop = set()
    for key_var in key_vars:
        key_vars_before_loop.add(get_ssa_var_name(key_var, var_counter[key_var]))
    for var_name in var_counter:
        ssa_dict_before_loop[var_name] = get_ssa_var_name(var_name, var_counter[var_name])

    old_var_counter = copy.deepcopy(var_counter)
    # 4. 处理G
    loop_item:LoopNode = path_to_loop[-1]
    g_expr = loop_item.guard
    g_code = transform_right_expr(g_expr, var_type_dict, var_counter)
    # cmps = first_comparison_sign(g_expr, key_vars)
    # if cmps is not None:
    #     iter_var, op = cmps
    #     iter_var_ssa = get_ssa_var_name(iter_var, var_counter[iter_var])
    #     iter_var_ssa_before = get_ssa_var_name(iter_var, var_counter[iter_var]-1)
    #     if op == -1:
    #         g_code = f"{g_code}, {iter_var_ssa} >= {iter_var_ssa_before}"
    #     elif op == +1:
    #         g_code = f"{g_code}, {iter_var_ssa} <= {iter_var_ssa_before}"
    # dprint("g_code:", g_code)

    # 5. 处理Trans
    trans_ir = loop_item.body
    trans_code, quantifier_binder_var_set = handle_stringfy_items(trans_ir, var_type_dict, var_counter, old_var_counter, declared_vars, loops_invs, loops_key_vars, solver_add=False)
    # for binder_var in quantifier_binder_var_set:
    #     if binder_var not in var_type_dict:
    #         var_type_dict[binder_var] = ("int",)
    #         var_counter[binder_var] = 0

    # print(trans_code)

    # 6. 保存进行一次循环体后的变量ssa状态
    key_vars_after_trans = set()
    for key_var in key_vars:
        key_vars_after_trans.add(get_ssa_var_name(key_var, var_counter[key_var]))
    for var_name in var_counter:
        ssa_dict_after_trans[var_name] = get_ssa_var_name(var_name, var_counter[var_name])

    # 7. 公共的代码
    PRE = f"And(\n{pre_code}\n)"
    G = f"And(\n{g_code}\n)"
    TRANS = f"And(\n{trans_code})"

    # 8. 创建无后置条件的DECLARE、SAVE_COUNTEREXAMPLE
    declare_code_no_post = get_declare_code(var_type_dict, var_counter)
    save_counterexample_no_post = get_save_counterexample_code(var_type_dict, var_counter)
    DECLARE = f"{declare_code_no_post}"
    SAVE_COUNTEREXAMPLE = f"{save_counterexample_no_post}"

    # 9. 创建无后置条件的EVALUATE
    key_vars_after_pre = sorted(key_vars_after_pre)
    key_vars_before_loop = sorted(key_vars_before_loop)
    key_vars_after_trans = sorted(key_vars_after_trans)
    EVALUATE = f'''# === 1. 前置条件证明 ===
__solver.push()
__solver.add(
    PRE, 
    Not(INV( {",".join(key_vars_after_pre)}, {",".join(key_vars_after_pre)} )),
)
check(__solver, 0)
__solver.pop()
                             
# === 2. 循环不变式保持性证明 ===
__solver.push()
__solver.add(
    PRE,
    INV( {",".join(key_vars_before_loop)}, {",".join(key_vars_after_pre)} ),
    G,
    TRANS,
    Not(INV( {",".join(key_vars_after_trans)}, {",".join(key_vars_after_pre)}  ))
)
check(__solver, 1)
__solver.pop()'''
    
    old_params = ",".join([f"__old_{x}" for x in key_vars])
    inv_params = ",".join(key_vars) + "," + old_params
    # 10. 创建无后置条件的代码    
    z3_code_pre = Z3_CODE_TEMPLATE.substitute(
        PRE=PRE,G=G,TRANS=TRANS,
        INV_PARAMS=inv_params,
        DECLARE=DECLARE, 
        SAVE_COUNTEREXAMPLE=SAVE_COUNTEREXAMPLE,
        EVALUATE=EVALUATE,
        POST_CODE="",
    )

    # 11. 如果有assert，创建后置条件代码
    # TODO 暂时没做后置条件有trans
    post_fol = loop_item.post_condition
    z3_code_post = ""
    if post_fol:
        # for var in var_type_dict:
        #     if var in key_vars:
        #         var_counter[var] += 1
        key_vars_after_loop = set()
        for key_var in key_vars:
            key_vars_after_loop.add(get_ssa_var_name(key_var, var_counter[key_var]))
        for var_name in var_counter:
            ssa_dict_after_loop[var_name] = get_ssa_var_name(var_name, var_counter[var_name])
        key_vars_after_loop = sorted(key_vars_after_loop)

        # assert的转换
        post_fol = replace_old(post_fol, old_var_counter, declared_vars)
        post_z3_s, quantifier_binder_var_set = transform_ssa_inv(post_fol, var_type_dict, var_counter)
        # for binder_var in quantifier_binder_var_set:
        #     if binder_var not in var_type_dict:
        #         var_type_dict[binder_var] = ("int",)
        #         var_counter[binder_var] = 0
        # 防止临时变量没有加入ssa
        # post_z3_s, quantifier_binder_var_set = transform_ssa_inv(post_fol, var_type_dict, var_counter)

        POST_CODE = f'''G_EXIT=Not({transform_right_expr(g_expr, var_type_dict, var_counter)})
        
POST={post_z3_s}'''
        
        EVALUATE_WITH_POST = f'''# === 3. 循环不变式后置条件证明(optional) ===
__solver.push()
__solver.add(
    PRE,
    INV({",".join(key_vars_after_loop)}, {",".join(key_vars_after_pre)}),
    G_EXIT,
    Not(POST)
)
check(__solver, 2)
__solver.pop()'''
        
        EVALUATE_WITH_POST = EVALUATE + "\n\n" + EVALUATE_WITH_POST

        declare_code_with_post = get_declare_code(var_type_dict, var_counter)
        save_counterexample_with_post = get_save_counterexample_code(var_type_dict, var_counter)
        DECLARE_WITH_POST = f"{declare_code_with_post}"
        SAVE_COUNTEREXAMPLE_WITH_POST = f"{save_counterexample_with_post}"
    

        z3_code_post = Z3_CODE_TEMPLATE.substitute(
            PRE=PRE,G=G,TRANS=TRANS,
            INV_PARAMS=inv_params,
            DECLARE=DECLARE_WITH_POST, SAVE_COUNTEREXAMPLE=SAVE_COUNTEREXAMPLE_WITH_POST,
            EVALUATE=EVALUATE_WITH_POST,
            POST_CODE=POST_CODE,
        )

    def write_code(output_file:str, z3_code:str):
        with open(output_file, "w") as f:
            f.write(z3_code)
        result = format_py(output_file)
        if result != None:
            raise Exception(result)
        
    write_code(pre_task_template_path, z3_code_pre)
    if z3_code_post != "":
        write_code(post_task_template_path, z3_code_post)
    # TODO 约束简化
    codes = ()
    return (
        codes, 
        (ssa_dict_after_pre, ssa_dict_before_loop, ssa_dict_after_trans, ssa_dict_after_loop)
    )
    