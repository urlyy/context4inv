from z3 import *

n, i, s = Ints('n i s')
solver = Solver()

# 程序：计算 1+2+...+n
# 后置条件：s == n*(n+1)/2

# 有问题的循环不变式集合
def problematic_invariant(n, i, s):
    return And(
        s > 0,                      # I1: 正确但弱
        i >= 1,                     # I2: 正确
        n >= 1,                     # I3: 前置条件
        i <= n + 1,                 # I4: 正确但弱
        # s >= n*(n+1)/2 + 1,        # I5: 错误！
        # 2*s == n*(n+1),
        s == s,                     # I6: 恒真但无用
        i + s > 0,                  # I7: 正确但弱
    )

print("=== 检查迭代保持 ===")
solver.push()
# 迭代前满足不变式
solver.add(problematic_invariant(n, i, s))
# 循环条件
solver.add(i <= n)
# 循环体
i1 = i + 1
s1 = s + i
n1 = n
# 假设迭代后不满足不变式
solver.add(Not(problematic_invariant(n1, i1, s1)))

if solver.check() == sat:
    m = solver.model()
    print("找到反例，不变式不保持")
    print(f"迭代前: n={m[n]}, i={m[i]}, s={m[s]}")
    print(f"执行后: n={m.evaluate(n1)}, i={m.evaluate(i1)}, s={m.evaluate(s1)}")
    
    print("\n检查哪个子式被违反:")
    for name, inv in [
        ("I1: s > 0", lambda n,i,s: s > 0),
        ("I2: i >= 1", lambda n,i,s: i >= 1),
        ("I3: n >= 1", lambda n,i,s: n >= 1),
        ("I4: i <= n+1", lambda n,i,s: i <= n + 1),
        # ("I5: s >= n*(n+1)/2 + 1", lambda n,i,s: s >= n*(n+1)/2 + 1),
        ("I6: s == s", lambda n,i,s: s == s),
        ("I7: i+s > 0", lambda n,i,s: i + s > 0)
    ]:
        s2 = Solver()
        # 设置迭代前的值
        s2.add(n == m[n], i == m[i], s == m[s])
        # 设置迭代后的值
        s2.add(n1 == m.evaluate(n1), i1 == m.evaluate(i1), s1 == m.evaluate(s1))
        # 检查迭代后是否违反该子式
        s2.add(Not(inv(n1, i1, s1)))
        
        if s2.check() == sat:
            print(f"  ✗ {name} 被违反")
            # 显示具体值
            m2 = s2.model()
            print(f"    迭代后: n={m2[n1]}, i={m2[i1]}, s={m2[s1]}")
        else:
            print(f"  ✓ {name} 保持")
else:
    print("不变式在迭代中保持")
solver.pop()

print("\n=== 检查后置条件 ===")
solver.push()
solver.add(problematic_invariant(n, i, s))
solver.add(Not(i <= n))  # 退出条件
solver.add(Not(s == n*(n+1)/2))  # 否定后置条件

if solver.check() == sat:
    m = solver.model()
    print("不变式不能推出后置条件")
    print(f"反例状态: n={m[n]}, i={m[i]}, s={m[s]}")
    expected = m.evaluate(n*(n+1)/2)
    print(f"期望 s = n*(n+1)/2 = {expected}")
    print(f"实际 s = {m[s]}")
    
    print("\n检查各子式是否满足:")
    for name, inv in [
        ("I1: s > 0", lambda n,i,s: s > 0),
        ("I2: i >= 1", lambda n,i,s: i >= 1),
        ("I3: n >= 1", lambda n,i,s: n >= 1),
        ("I4: i <= n+1", lambda n,i,s: i <= n + 1),
        # ("I5: s >= n*(n+1)*2 + 1", lambda n,i,s: s >= n*(n+1)*2 + 1),
        # ("I5: 2*s == n*(n+1)", lambda n,i,s: 2*s == n*(n+1)),
        ("I6: s == s", lambda n,i,s: s == s),
        ("I7: i+s > 0", lambda n,i,s: i + s > 0)
    ]:
        s2 = Solver()
        s2.add(n == m[n], i == m[i], s == m[s])
        s2.add(inv(n, i, s))
        if s2.check() == unsat:
            print(f"  ✗ {name} 不满足")
        else:
            print(f"  ✓ {name} 满足")
else:
    print("不变式能推出后置条件")
solver.pop()

# print("\n=== 单独检查每个子式作为不变式的可行性 ===")
# for name, inv in [
#     ("I1: s > 0", lambda n,i,s: s > 0),
#     ("I2: i >= 1", lambda n,i,s: i >= 1),
#     ("I3: n >= 1", lambda n,i,s: n >= 1),
#     ("I4: i <= n+1", lambda n,i,s: i <= n + 1),
#     ("I5: s >= n*(n+1)/2 + 1", lambda n,i,s: s >= n*(n+1)/2 + 1),
#     ("I6: s == s", lambda n,i,s: s == s),
#     ("I7: i+s > 0", lambda n,i,s: i + s > 0)
# ]:
#     solver.push()
#     # 测试迭代保持
#     solver.add(inv(n, i, s))  # 迭代前
#     solver.add(i <= n)        # 循环条件
#     i1 = i + 1
#     s1 = s + i
#     n1 = n
#     solver.add(Not(inv(n1, i1, s1)))  # 假设迭代后违反
    
#     if solver.check() == unsat:
#         result = "可作为不变式"
#     else:
#         result = "不能作为不变式"
#     solver.pop()
    
#     # 检查是否能推出后置条件
#     solver.push()
#     solver.add(inv(n, i, s))  # 退出时满足
#     solver.add(Not(i <= n))   # 退出条件
#     solver.add(Not(s == n*(n+1)/2))  # 否定后置条件
    
#     if solver.check() == unsat:
#         cond_result = "能推出后置条件"
#     else:
#         cond_result = "不能推出后置条件"
#     solver.pop()
    
#     print(f"{name}: {result}, {cond_result}")