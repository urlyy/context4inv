from tree_sitter import Node
import os
import inspect

def node2str(node:Node):
    return node.text.decode("utf-8")

def unimplement(log:str=""):
    raise Exception(f"unimplement: {log}")

def first_capitalize(s:str)->str:
    return s[0].upper() + s[1:]


# TY_TRANSFORM = "trans"
# TY_TRANS_ARR = "trans_arr"
# TY_TRANS_POINTER = "trans_pointer"
# # dereference
# TY_TRANS_DEPOINTER = "trans_depointer"
# TY_IF = "if"
# TY_LOOP = "loop"
# TY_RET = "return"
# TY_IF_COND = "if_cond"
# TY_DECLARE = "declare"
# TY_ASSUME = "assume"
# TY_ASSERT = "assert"

TAB = '\t'
VAR = "var"
VAR_ARRAY = "array"
VAR_POINTER = "pointer"

os.environ['DPRINT_LOCATION'] = '1'
# os.environ['DPRINT_ENABLED'] = '0'

# 5s
timeout_solve = 10

def dprint(*args, **kwargs):
    """
    一个可根据环境变量控制的打印函数。

    环境变量:
    - DPRINT_ENABLED: 设置为 "1" 或 "true" (不区分大小写) 时，启用打印功能。
                      默认为启用。
    - DPRINT_LOCATION: 设置为 "1" 或 "true" (不区分大小写) 时，在打印内容前
                         输出调用dprint所在的文件和行号。默认为不输出位置。
    """
    # 检查内容打印功能是否启用
    enabled_str = os.environ.get('DPRINT_ENABLED', '1').lower()
    is_enabled = enabled_str in ['1', 'true']

    if not is_enabled:
        return

    # 检查位置信息打印功能是否启用
    location_str = os.environ.get('DPRINT_LOCATION', '0').lower()
    show_location = location_str in ['1', 'true']

    if show_location:
        # 获取调用者的栈帧信息
        # inspect.stack() 返回一个列表，[0]是当前函数dprint, [1]是调用dprint的函数
        try:
            caller_frame = inspect.stack()[1]
            filename = caller_frame.filename
            lineno = caller_frame.lineno
            location_prefix = f"[{os.path.basename(filename)}:{lineno}] "
        except IndexError:
            location_prefix = "[<unknown file>:<unknown line>] "
        
        # 将位置信息添加到打印内容的最前面
        print(location_prefix, end='')

    # 打印用户传入的实际内容
    print(*args, **kwargs)