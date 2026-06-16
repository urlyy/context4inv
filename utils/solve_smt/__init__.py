import os
import subprocess
import traceback
from utils.solve_smt.path2z3 import __path2z3
from pathlib import Path
import sys
import json
import time
from common import timeout_solve

from utils.format_py import format_py

def path2z3(path_to_loop:list, key_vars:list[str], var_type_dict:dict, loops_invs:list[set[str]], loops_key_vars:list[list[str]], func_spec_dict:dict, pre_task_template_path, post_task_template_path):
    codes, ssa_dicts = __path2z3(path_to_loop, key_vars, var_type_dict, loops_invs, loops_key_vars, func_spec_dict, pre_task_template_path, post_task_template_path)
    return codes, ssa_dicts

def solve_smt(filled_solve_file:str)->tuple[bool,str|dict,float]:
    file_path = Path(filled_solve_file)
    dir = file_path.parent
    file_name_without_ext = file_path.stem

    format_res = format_py(filled_solve_file)
    if format_res != None:
        return False, format_res, 0
   
    counterexample_output_file = os.path.join(dir, f"{file_name_without_ext}_counterexample.json")
    # if os.path.exists(counterexample_output_file):
    #     os.remove(counterexample_output_file)
    # run solve
    command= ["python", filled_solve_file, counterexample_output_file]
    start_time = time.perf_counter()
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout_solve,
        )
    except subprocess.TimeoutExpired:
        raise Exception(f"{filled_solve_file} occurs timeout.")
    elapsed_time = time.perf_counter() - start_time
    ret_code = result.returncode
    if ret_code == 0:
        return True, "", elapsed_time
    elif ret_code == 1:
        raise Exception(result.stderr)
    elif ret_code == 14:
        with open(counterexample_output_file, "r") as f:
            counterexample = f.read()
            data = json.loads(counterexample)
            print(f"脚本运行时间: {elapsed_time:.6f} 秒")
            return False, (data["reason"], True, data["unknown_reason"]), elapsed_time
        # raise Exception("求解结果为unknown, 丢弃该不变式")
    elif ret_code == 13:
        with open(counterexample_output_file, "r") as f:
            counterexample = f.read()
            data = json.loads(counterexample)
            print(f"脚本运行时间: {elapsed_time:.6f} 秒")
            return False, (data["reason"], False, data["counterexample"]), elapsed_time
    else:
        raise Exception("Unexpected return code: " + str(ret_code), result.stdout, result.stderr)