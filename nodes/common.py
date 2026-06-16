from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
import shutil
from langgraph.graph import MessagesState, StateGraph
from typing import Optional
from langchain_core.language_models.llms import LLM
from langchain_core.messages import SystemMessage, BaseMessage
from utils.fol_parser import fol_to_z3
from utils.cparser import Node
from collections import deque
from common import dprint, node2str, unimplement
from typing import TypedDict
from utils.z3_model_to_nl import z3_model_to_nl

class IRNode:
    pass

class LoopNode(IRNode):
    guard: str
    body: list[IRNode]
    depth: int
    loop_id: int
    post_condition: str | None
    # post_assumes: list[str]
    var_deps: dict[str, set[str]]
    
    def __init__(self, guard, body, depth, loop_id, post_condition, var_deps):
        self.guard = guard
        self.body = body
        self.depth = depth
        self.loop_id = loop_id
        self.post_condition = post_condition
        # self.post_assumes = post_assumes
        self.var_deps = var_deps

    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        body_str = ",".join(str(node) for node in self.body)
        s = f"Loop(id={self.loop_id},depth={self.depth},guard={self.guard},body=[{body_str}]"
        # if self.post_assumes:
        #     s += f",post_assumes=[{','.join(self.post_assumes)}]"
        if self.post_condition:
            s += f",post='{self.post_condition}'"
        s += ")"
        if self.var_deps:
            s += f",var_deps={self.var_deps}"
        return s


class MessageData(TypedDict):
    pass


class GlobalData(TypedDict):
    inverted_call_graph: dict[str,set[str]]
    func_to_visit_queue: deque[str]
    func_node_dict: dict[str,Node]
    fol_msg: SystemMessage

class FuncData(TypedDict):
    cur_name:str
    cur_node:Node
    ret_type:str
    body_ir:list
    var_type_dict:dict
    path_to_loops:list[list[IRNode]]
    loop_nodes:list[Node]
    # 会变的
    loops_invs:list[set[str]]
    loops_key_vars:list[set[str]]
    loops_counterexample_vars:list[set[str]]
    loops_ssa_dicts:list[dict[str,str]]

    gen_err:bool

class LoopData(TypedDict):
    cur_id: int
    key_vars:list[str]
    counterexample_vars:set[str]
    path_to_loop:list[IRNode]
    ssa_dict_after_pre: dict[str,str]
    ssa_dict_before_loop: dict[str,str]
    ssa_dict_after_trans: dict[str,str]
    ssa_dict_after_loop: dict[str,str]
    loop_code_msg: SystemMessage
    
class Task1Data(TypedDict):
    try_count: int
    valid_invariants: dict[str,set[str]]
    llm_gen: dict[str,set[str]]
    has_counterexample: bool
    # key_var => [(inv1,reason,counter), ...]
    counterexamples: dict[str,list[tuple[str,int,dict]]]
    format_msg: SystemMessage
    msgs:list[BaseMessage]

class Task2Data(TypedDict):
    try_count: int
    valid_invariants: set[str]
    llm_gen: set[str]
    has_counterexample: bool
    # key_var => [(inv1,reason,counter), ...]
    counterexamples: list[tuple[str,int,dict]]
    format_msg: SystemMessage
    msgs:list[BaseMessage]


class Task12Data(TypedDict):
    try_count: int
    valid_invariants: set[str]
    llm_gen: set[str]
    has_counterexample: bool
    counterexamples: list[tuple[str,int,dict]]
    format_msg: SystemMessage
    msgs:list[BaseMessage]

class Task3Data(TypedDict):
    try_count: int
    has_counterexample: bool
    llm_gen: set[str]
    valid_invariants: set[str]
    counterexample: tuple[str,int,dict]
    format_msg: SystemMessage
    msgs:list[BaseMessage]

class Task4Data(TypedDict):
    try_count: int
    has_counterexample: bool
    ce_and_loop_id: tuple[int, dict, int]
    llm_gen: dict[str,list[str]]
    # valid_invariants: set[str]
    # counterexample: tuple[str,int,dict]
    format_msg: SystemMessage
    msgs:list[BaseMessage]
    smallest_modified_loop_id: int

class CommonData(TypedDict):
    counterexample: any
    

class AgentState(MessagesState):
    global_data: GlobalData
    func_data: FuncData
    loop_data: LoopData
    task1_data: Task1Data
    task2_data: Task2Data
    task12_data: Task12Data
    task3_data: Task3Data
    task4_data: Task4Data
    # # msg
    # # fol格式
    # global_sys_msg: SystemMessage
    # # 当前循环结尾行以上的代码(循环已被替换)
    # loop_sys_msg: SystemMessage
    # # 两个任务的格式要求 
    # sys_msg_each: SystemMessage
    # sys_msg_combined: SystemMessage
    # sys_msg_post: SystemMessage
    # messages_each: list[BaseMessage]
    # messages_combined: list[BaseMessage]
    # messages_post: list[BaseMessage]

    # llm_gen_invariants_each:dict[str,list[str]]
    # llm_gen_invariants_combined:list[str]
    # llm_gen_invariants_post:list[str]
    # invariants_with_counterexample_each:dict[str,dict[str,dict]]
    # invariants_with_counterexample_combined:dict[str,dict]
    # counterexample_post:tuple[int,dict]
    # invariants_each:dict[str,set[str]]
    # invariants_combined:set[str]
    # invariants_pre:list[str]
    # invariants_post:list[str]
    
    # loop_key_vars: list[str]
    # has_assert: bool
    # ssa_dict_after_pre: dict[str,str]
    # ssa_dict_before_loop: dict[str,str]
    # ssa_dict_after_loop: dict[str,str]
    # var_type_dict: dict[str, tuple]

    # # func scope usable
    # # 函数IR
    # func_info: list
    # # 每个函数内从起点到每个循环的路径
    # path_to_loops:list[list]
    # # 当前处理的循环的路径下标
    # loop_id: int
    # # 循环id->loop_node
    # func_loop_id_dict: dict[int, Node]
    # rev_func_loop_id_dict: dict[Node, int]
    # func_loops_invs: list[list[str]]

    # loops_key_vars: list[list[str]]

    # # global usable
    # # 函数调用图（反转为自底向上）
    # inverted_call_graph: dict[str,set[str]]
    # # 当前处理的函数名
    # cur_handled_func: str
    # # 基于调用图bfs生成的处理顺序队列
    # func_to_visit_queue: deque[str]
    # # 函数名->treesitter函数结点
    # func_node_dict: dict[str, Node]
    # # func_name -> loops[invs[]]
    # global_loop_inv_dict: dict[str,list[list[str]]]
    
   

    
    # template_file_path:str

    # has_counterexample_each:bool
    # has_counterexample_combined:bool
    # has_counterexample_post:bool

    # try_count_each:int
    # try_count_combined:int
    # try_count_post:int
    # err_log: Optional[str]
    # err_code: int


    # # z3_init_code:str
    # # z3_pre_code:str
    # # z3_const_code:str
    # # z3_pre_code:str
    # # z3_g_code:str
    # # z3_t_code:str


class AssumeNode(IRNode):
    expr: str
    def __init__(self, expr):
        self.expr = expr
    
    def __str__(self):
        return f"Assume({self.expr})"
    
    def __repr__(self):
        return self.__str__()
    
# class AssumeInvariantNode(IRNode):
#     expr: str
#     loop_id: int
#     def __init__(self, loop_id, expr):
#         self.expr = expr
#         self.loop_id = loop_id
    
#     def __str__(self):
#         return f"AssumeInvariant(LOOP-{self.loop_id},{self.expr})"
    
#     def __repr__(self):
#         return self.__str__()

class AssertNode(IRNode):
    expr: str
    def __init__(self, expr):
        self.expr = expr
    
    def __str__(self):
        return f"Assert({self.expr})"
    
    def __repr__(self):
        return self.__str__()

class TransNode(IRNode):
    left_var: str
    right_val: str
    def __init__(self, left_var, right_val):
        self.left_var = left_var
        self.right_val = right_val
    
    def __str__(self):
        return f"Trans({self.left_var}={self.right_val})"
    
    def __repr__(self):
        return self.__str__()
    
class DeclareNode(IRNode):
    var_name: str
    def __init__(self, var_name):
        self.var_name = var_name
    
    def __str__(self):
        return f"Declare({self.var_name})"
    
    def __repr__(self):
        return self.__str__()
    
class FuncParamDeclareNode(IRNode):
    var_name: str
    def __init__(self, var_name):
        self.var_name = var_name
    
    def __str__(self):
        return f"FuncParamDeclare({self.var_name})"
    
    def __repr__(self):
        return self.__str__()
    
class TransArrNode(IRNode):
    left_arr: str
    index: str
    right_val: str
    def __init__(self, left_arr, index, right_val):
        self.left_arr = left_arr
        self.index = index
        self.right_val = right_val
    
    def __str__(self):
        return f"TransArr({self.left_arr}[{self.index}]={self.right_val})"
    
    def __repr__(self):
        return self.__str__()
    

class IfNode(IRNode):
    branches: list[tuple[str, list[IRNode]]]
    def __init__(self, branches):
        self.branches = branches
    
    def __str__(self):
        branch_strs = []
        for cond, nodes in self.branches:
            node_strs = "\n".join("  " + str(node) for node in nodes)
            branch_strs.append(f"If({cond}):\n{node_strs}")
        return "\n".join(branch_strs)
    
    def __repr__(self):
        return self.__str__()

class IfCondNode(IRNode):
    expr: str
    def __init__(self, expr):
        self.expr = expr
    
    def __str__(self):
        return f"IfCond({self.expr})"
    
    def __repr__(self):
        return self.__str__()
    
class OuterLoopGuardNode(IRNode):
    expr: str
    loop_id: int
    def __init__(self, expr, loop_id):
        self.expr = expr
        self.loop_id = loop_id
    
    def __str__(self):
        return f"Loop_{self.loop_id}_Guard({self.expr})"
    
    def __repr__(self):
        return self.__str__()

# 处理大模型返回的json
def clean_json(json_str):
    """
    提取 JSON 块或 answer 代码块内容。
    
    优先级：
    1. ```answer …``` 代码块
    2. 最外层 JSON 块 { … } 或 [ … ]，支持嵌套
    """
    # 1. 尝试提取 ```answer …``` 代码块
    match = re.search(r'```answer\s*\n([\s\S]*?)```', json_str, re.MULTILINE)
    if match:
        return match.group(1).strip()
    
    # 2. 尝试提取最外层 JSON 块
    stack = []
    start = None
    for i, c in enumerate(json_str):
        if c in '{[':
            if not stack:
                start = i
            stack.append(c)
        elif c in '}]':
            if not stack:
                continue
            open_c = stack.pop()
            if (open_c == '{' and c != '}') or (open_c == '[' and c != ']'):
                raise ValueError("括号不匹配")
            if not stack:
                return json_str[start:i+1].strip()
    
    # 3. 没有找到匹配块，返回空字符串
    return ''

def get_semantic_explain(code_snippet: str, invariant, state_values: str, failure_type: str = "Preservation"):
    from utils.zhipu import llm
    from langchain.prompts import ChatPromptTemplate

    template = """
  ### Role
You are a Precise Mathematical Auditor. 

### Analysis Logic
The current invariant {invariant} failed. 
Step 1: Substitute values {state_values} into the formula.
Step 2: Show the conflict (e.g., LHS 0 != RHS 50).

### Output Constraints
- DO NOT suggest complex logic or quantifiers.
- Identify if the error is a "Variable Mismatch" (e.g., using y instead of w).
- Keep the diagnosis to exactly two parts: Diagnosis and Hint.

### Example Output
Diagnosis: Calculation error. In 'z == x * y', plugging in x=5, y=10, z=0 results in 0 == 50 (False).
Hint: The formula is using the limit 'y'. Replace it with the current counter 'w' to get 'z == x * w'.
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    
    # 构造 Chain
    chain = prompt | llm
    
    # 执行并获取结果
    response = chain.invoke({
        "code_snippet": code_snippet,
        "invariant": invariant,
        "state_values": state_values,
        "failure_type": failure_type
    })
    
    # 如果是对象则取 content，如果是字符串直接返回
    return response.content if hasattr(response, 'content') else str(response)



# def load_llm_gen(s:str):
#     cleaned_json = clean_json(s)
#     invariants = json.loads(cleaned_json)

'''
Description:
    获得markdown形式的表格
Example:
    h = ['ID', 'Name', 'Score']
    r = [(1, 'Tom', 98), (2, 'Lucy', 87)]
    md_table(h, r)
'''
def md_table(headers: list[str], rows: list[tuple], invariant, reason) -> str:
    def row(r): return '| ' + ' | '.join(map(str, r)) + ' |'
    lines = [row(headers),
             row(['-' * len(str(h)) for h in headers])]
    lines.extend(row(r) for r in rows)

    res = '\n'.join(lines)

    code_snippet = '''
int main() {
	int x, y, z, w;
	//@ assume(x >= 0 && y >= x)
	z = 0;
	w = 0;
	while(w < y) {
		z += x;
		w += 1;
	}
	//@ assert(z == x * y)
	return 0;
}

'''.strip()
    
    if reason == 0:
        phase = "Initialization"
    elif reason == 1:
        phase = "Preservation"
    else:
        phase = "Post-condition"
    
    # res += "\n" + get_semantic_explain(code_snippet, invariant, res, phase)
    return res

def get_value(value: str):
    # if "Store" in value or "K(Int" in value or "Lambda(" in value:
    #     return z3_model_to_nl(value)
    return value


def get_experiment_switches(config) -> dict:
    configurable = (config or {}).get("configurable", {})
    exp_cfg = configurable.get("experiment", {}) or {}
    mode = str(exp_cfg.get("mode", "full")).strip().lower()
    if mode not in ("full", "task12_only", "no_iterative", "c"):
        mode = "full"

    iterative = mode != "no_iterative"
    use_task12_only = mode == "task12_only"
    enable_task4_pre_enhance = mode != "no_task4_pre_enhance"
    # Explicit experiment flag takes precedence over mode defaults.
    if "enable_task4_pre_enhance" in exp_cfg:
        enable_task4_pre_enhance = bool(exp_cfg.get("enable_task4_pre_enhance"))

    llm_retry_limit = exp_cfg.get("llm_retry_limit", 5)
    try:
        llm_retry_limit = int(llm_retry_limit)
    except Exception:
        llm_retry_limit = 5
    if llm_retry_limit < 1:
        llm_retry_limit = 1

    switches = {
        "mode": mode,
        "enable_task1": not use_task12_only,
        "enable_task2": not use_task12_only,
        "enable_task12": use_task12_only,
        "enable_iterative": iterative,
        "enable_task4_pre_enhance": enable_task4_pre_enhance,
        "llm_retry_limit": llm_retry_limit,
        "task1_retry_limit": llm_retry_limit,
        "task2_retry_limit": llm_retry_limit,
        "task12_retry_limit": llm_retry_limit,
        "task3_retry_limit": llm_retry_limit,
        "task4_retry_limit": llm_retry_limit,
    }
    return switches

# 不变式涉及的所有变量，以及未包含在内的关键变量
def get_true_counterexample(invariant, counterexample_vars, counterexample:dict, reason:int, ssa_dicts:list[dict]) -> dict:
    if reason == 0:
        ssa_dict = ssa_dicts[0]
        headers = ['variable', 'value_at_loop_entry']
        rows = list()
        for var, ssa_var in ssa_dict.items():
            if var in counterexample_vars or re.search(rf'\b{var}\b', invariant):
                tmp = counterexample.get(ssa_var)
                if tmp:
                    rows.append( (var, get_value(tmp)) )
        res = md_table(headers, rows, invariant, reason)
    elif reason == 1:
        ssa_dict_before_iteration = ssa_dicts[1]
        ssa_dict_after_iteration = ssa_dicts[2]
        headers = ['variable', 'value_before_iteration', 'value_after_iteration']
        rows = list()
        for var, ssa_var_before_iteration in ssa_dict_before_iteration.items():
            if var in counterexample_vars or re.search(rf'\b{var}\b', invariant):
                tmp = counterexample.get(ssa_var_before_iteration)
                ssa_var_after_iteration = ssa_dict_after_iteration[var]
                tmp2 = counterexample.get(ssa_var_after_iteration)
                if tmp and tmp2:
                    rows.append( (var, get_value(tmp), get_value(tmp2)) )
        res = md_table(headers, rows, invariant, reason)
    elif reason == 2:
        ssa_dict = ssa_dicts[3]
        headers = ['variable', 'value_at_loop_exit']
        rows = list()
        for var, ssa_var in ssa_dict.items():
            if var in counterexample_vars or re.search(rf'\b{var}\b', invariant):
                tmp = counterexample.get(ssa_var)
                if tmp:
                    rows.append( (var, get_value(tmp)) )
        res = md_table(headers, rows, invariant, reason)
    else:
        unimplement("get_true_counterexample 有问题")
    
    
    # dprint("-"*70)
    # dprint(invariant)
    # dprint(key_vars)
    # dprint(counterexample)
    # dprint(ssa_dict)
    # dprint(true_data)
    # dprint("-"*70)
    return res + "\n"

# invariant = "0 <= i && i < n"
# key_vars = {"i"}
# counterexample = {'n_0': '0', 'k_0': '0', 'i_1': '0'}
# ssa_dict_before_loop = {'n': 'n_0', 'k': 'k_0', 'i': 'i_1'}
# print(get_true_counterexample(invariant, key_vars, counterexample, ssa_dict_before_loop))

def conjuct_invariants(invarinats:list[str])->str:
    new_invarinats = [f"({inv})" for inv in invarinats]
    return " && ".join(new_invarinats)

def __get_quantifier_binder_var_init_code(quantifier_binder_var_set:set[str]):
    if len(quantifier_binder_var_set) == 0:
        return ""
    new_names = []
    for orig_name in quantifier_binder_var_set:
        new_names.append(orig_name)
    left_names = ','.join(new_names)
    # 构成列表
    if len(new_names) == 1:
        left_names += ","
    init_code = f'''{left_names}=Ints("{' '.join(new_names)}")'''
    return init_code

# ssa_dict只取常量，所以三个中任意一个都可以
def trans_invariant(invariant, key_vars, ssa_dict):
    ssa_invariant = invariant
    # var_sort_dict = dict()
    _, quantifier_binder_var_set = fol_to_z3(ssa_invariant)
    new_binder_var_set = set()
    for binder_var in quantifier_binder_var_set:
        if binder_var not in ssa_dict:
            new_binder_var_set.add(binder_var)
    # 做变量替换
    for orig_var,ssa_var in ssa_dict.items():
        pattern = rf"\b{orig_var}\b"
        if re.search(pattern, invariant):
            if orig_var in key_vars:
                ssa_var = orig_var
            else:
                ssa_var = ssa_dict[orig_var]
            ssa_invariant = re.sub(pattern, ssa_var, ssa_invariant)
                # var_sort = __get_sort(var_type_dict[orig_var])
                # var_sort_dict[ssa_var] = var_sort
    z3_invariant, _ = fol_to_z3(ssa_invariant)
    quantifier_binder_var_init_code = __get_quantifier_binder_var_init_code(new_binder_var_set)
    return quantifier_binder_var_init_code, z3_invariant, z3_invariant


def get_func_subject_dir(config, func_name, create=False):
    output_dir = config["configurable"].get("output_dir")
    subject_dir = os.path.join(output_dir, f"FUNC_{func_name}")
    if create:
        if os.path.exists(subject_dir):
            shutil.rmtree(subject_dir)
        os.mkdir(subject_dir)
    return subject_dir

def get_loop_subject_dir(config, func_name, loop_id, create=False):
    func_subject_dir = get_func_subject_dir(config, func_name)
    loop_subject_dir = os.path.join(func_subject_dir, f"LOOP_{loop_id}")
    if create:
        # if os.path.exists(loop_subject_dir):
        #     shutil.rmtree(loop_subject_dir)
        os.mkdir(loop_subject_dir)
    return loop_subject_dir

def get_tmp_code_path(config, func_name, loop_id, create=False):
    loop_subject_dir = get_loop_subject_dir(config, func_name, loop_id)
    file_path = os.path.join(loop_subject_dir, "tmp_code.c")
    if create:
        open(file_path, "w").close()
    return file_path

def get_pre_task_z3_template_path(config, func_name, loop_id, create=False):
    loop_subject_dir = get_loop_subject_dir(config, func_name, loop_id)
    file_path = os.path.join(loop_subject_dir, "z3_template_pre.py")
    if create:
        open(file_path, "w").close()
    return file_path

def get_post_task_z3_template_path(config, func_name, loop_id, create=False):
    loop_subject_dir = get_loop_subject_dir(config, func_name, loop_id)
    file_path = os.path.join(loop_subject_dir, "z3_template_post.py")
    if create:
        open(file_path, "w").close()
    return file_path

def get_verify_dir(config, func_name, loop_id, create=False):
    loop_subject_dir = get_loop_subject_dir(config, func_name, loop_id)
    dir = os.path.join(loop_subject_dir, "verify")
    if create:
        # if os.path.exists(dir):
        #     shutil.rmtree(dir)
        os.mkdir(dir)
    return dir

def get_err_log_path(config, func_name, loop_id, create=False):
    loop_subject_dir = get_loop_subject_dir(config, func_name, loop_id)
    file_path = os.path.join(loop_subject_dir, "err.log")
    if create:
        # if os.path.exists(file_path):
        #     os.remove(file_path)
        open(file_path, "w").close()
    return file_path


# if __name__ == "__main__":
# # 测试用例
#     test_inputs = [
#    '''some_text,

#    [
#         "a[1]==1",
#         "a>0=>b>0"
#    ]
#     ''',

#      '''some_text,
#     ```json
#    [
        
#         "a[1]==1",
#         "a>0=>b>0"
#    ]
#    ```
#     ''',

#      '''some_text,

#    {
#         "a":["a[1]==1", "a[1]==1"],
#         "b": ["a>0=>b>0"]
#    }
#     ''',

#      '''some_text,
#     ```json
#    {
#         "a":["a[1]==1", "a[1]==1"],
#         "b": ["a>0=>b>0"]
#    }
#    ```
#     ''',

#     '''
# ```json
# {
#     "x": ["x == y * y"],
#     "y": ["y >= 0"]
# }
# ```
# '''
# ]

# # 执行测试
# for idx, text in enumerate(test_inputs, 1):
#     print(f"Test Case {idx}:\n{clean_json(text)}\n{'-'*40}")

def get_current_code(config, func_name, func_node: Node, target_loop_ir_node: LoopNode|None, loop_nodes:list[Node], loop_ir_nodes:list[LoopNode], func_loops_invs:list[list],  replace_loop_to_assume:bool, add_inv_comment=True, write_file=True):
    def is_loop_node(_node: Node) -> bool:
        return _node.type in ("for_statement", "while_statement", "do_statement")
    def __get_current_code(cur_node:Node, source_bytes, parts:list, finished=[False]):
        prev_child_end = cur_node.start_byte
        base_offset = func_node.start_byte
        if cur_node.child_count == 0:
            parts.append(node2str(cur_node))
            return
            # if cur_node.type == "comment":
            #     comment_text = node2str(cur_node)
            #     if comment_text.find("//@ assert") >= 0:
            #         comment_text = comment_text.replace("//@ assert", "//@ assume")
            #     parts.append(comment_text)
            # else:
            #     parts.append(node2str(cur_node))
        
        # 提前准备好label注释
        if is_loop_node(cur_node):
            loop_id = loop_nodes.index(cur_node)
            target_id = None
            if target_loop_ir_node is None:
                assert(not replace_loop_to_assume)
                target_id = len(func_loops_invs)
            else:
                target_id = target_loop_ir_node.loop_id
            if loop_id <= target_id:
                # 两种处理方式
                if replace_loop_to_assume:
                    if loop_id < target_id:
                        loop_ir_node = loop_ir_nodes[loop_id]
                        inv = conjuct_invariants( list(func_loops_invs[loop_id])+ [f"!({loop_ir_node.guard})"] )
                        parts.append(f"//@ ASSUME({inv})")
                        return
                    elif loop_id == target_id:
                        # 给循环添加label
                        parts.append(f"TARGET_LOOP:")
                else:
                    # parts[-1]是前一个结点到当前结点的间隔
                    indent = parts[-1]
                    # 只获得缩进
                    idx = indent.rfind('\n')
                    if idx != -1:
                        indent = indent[idx+1:]
                    indent = indent
                    # 两种情况
                    loop_name = f"LOOP_{loop_id}"
                    if loop_id < target_id:
                        inv = conjuct_invariants(func_loops_invs[loop_id])
                        # 使注释在循环上面一行
                        if add_inv_comment:
                            parts.append(f"//@ {loop_name} invariant: {inv}\n")
                            parts.append(indent)
                        # 给循环添加label
                        parts.append(f"{loop_name}:")
                    elif loop_id == target_id:
                        # 给循环添加label
                        parts.append(f"{loop_name}:")
        for i, child in enumerate(cur_node.children):
            # 当前结点和前面结点之间的换行和缩进
            indent:str = source_bytes[prev_child_end-base_offset:child.start_byte-base_offset].decode('utf8')
            parts.append(indent)
            # if finished[0]:
            #     # 在target_loop的父节点，处理它之后紧挨着的assert注释
            #     if child.type == "comment" and i > 0:
            #         pre_node = cur_node.children[i-1]
            #         if is_loop_node(pre_node) and loop_nodes.index(pre_node) == target_loop_ir_node.loop_id:
            #             parts.append(node2str(child))
            #     break 
            __get_current_code(child, source_bytes, parts, finished)
            prev_child_end = child.end_byte
        # 防止直接把后面本该截取的代码部分也添加进parts
        # if not finished[0]:
        #     # 最后一个结点和前面结点之间的换行和缩进
        #     parts.append(source_bytes[prev_child_end-base_offset:cur_node.end_byte-base_offset].decode('utf8'))
        if is_loop_node(cur_node): 
            loop_id = loop_nodes.index(cur_node)
            if loop_id == target_id:
                finished[0] = True
                
    parts = []
    __get_current_code(func_node, func_node.text, parts)
    code = ''.join(parts)

    tmp_code_path = None
    if replace_loop_to_assume:
        tmp_code_path = get_tmp_code_path(config, func_name, target_loop_ir_node.loop_id)
    if target_loop_ir_node is None:
        subject_dir = get_func_subject_dir(config, func_name)
        tmp_code_path = os.path.join(subject_dir, "FINAL_code.c")
    if tmp_code_path and write_file:
        with open(tmp_code_path, "w") as f:
            f.write(code)

        dprint(tmp_code_path)
        dprint(code)
    # exit()
    return code


def get_vars_from_str(expr: str):
    pattern = r'\b[A-Za-z_][A-Za-z0-9_]*\b'
    vars = re.findall(pattern, expr)
    return vars