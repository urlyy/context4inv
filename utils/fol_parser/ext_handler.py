import re

# only used in loop_invariant && assert, not in assume
def replace_old(s: str, old_counter: dict[str,int], declared_vars):
    # 过滤字典
    new_dict = {k: old_counter[k] for k in declared_vars if k in old_counter}
    
    # 匹配 old(var) 或 old(var[...])
    pattern = r'old\(\s*([a-zA-Z_]\w*)(\[[^\]]*\])?\s*\)'

    def repl(match):
        var = match.group(1)
        bracket = match.group(2) or ''
        if var not in new_dict:
            return f"{var}{bracket}"
            # raise KeyError(f"inv: {s}, 变量 {var} 不在字典{new_dict}中")
        return f"{var}_{new_dict[var]}{bracket}"

    return re.sub(pattern, repl, s)

def replace_old_for_solve(s: str, key_vars: set[str]):
    # return s
    pattern = r'old\(\s*([a-zA-Z_]\w*)(\[[^\]]*\])?\s*\)'
    def repl(match):
        var = match.group(1)
        bracket = match.group(2) or ''
        if var not in key_vars:
            return f"{var}{bracket}"
            # raise KeyError(f"inv: {s}, key_vars: {key_vars}, 变量 {var} 不在字典中")
        return f"__old_{var}{bracket}"
    return re.sub(pattern, repl, s)


if __name__ == "__main__":
    # 示例
    mapping = {"y": 1, "z": 5, "temp123": 9, "arr": 1}
    expr = "old(y) + old(z) + old(temp123) + old(arr[1])"
    print(replace_old(expr, mapping, {"y","temp123","z", "arr"}))
    # 输出: x = y_1 + z_5 + temp123_9 + arr_1[1]

    key_vars = {"y","temp123","z", "arr"}
    print(replace_old_for_solve(expr, key_vars))
