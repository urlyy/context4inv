from z3 import *

x, y = Ints('x y')
s = Solver()

# 定义四个子式，其中三个错误
I1 = lambda x,y: x + y == 10    # 正确的
I2 = lambda x,y: x > y + 5      # 错误的
I3 = lambda x,y: y > 0          # 错误的  
I4 = lambda x,y: x % 2 == 1     # 错误的

# 合取：I1 ∧ I2 ∧ I3 ∧ I4
combined = lambda x,y: And(I1(x,y), I2(x,y), I3(x,y), I4(x,y))

print("=== 情况1：合取为假，但I1可能为真 ===")
s.push()
s.add(combined(x, y))
if s.check() == unsat:
    print("合取不可满足，找不到model")
else:
    m = s.model()
    print(f"合取可满足: x={m[x]}, y={m[y]}")
    print(f"I1单独: {I1(m[x], m[y])}")
    print(f"I2单独: {I2(m[x], m[y])}")
    print(f"I3单独: {I3(m[x], m[y])}")
    print(f"I4单独: {I4(m[x], m[y])}")
s.pop()

print("\n=== 情况2：寻找满足I1但不满足其他三个的model ===")
s.push()
s.add(I1(x, y))        # I1正确
s.add(Not(I2(x, y)))   # I2错误
s.add(Not(I3(x, y)))   # I3错误  
s.add(Not(I4(x, y)))   # I4错误

if s.check() == sat:
    m = s.model()
    print(f"找到model: x={m[x]}, y={m[y]}")
    print(f"I1: x+y==10 -> {m[x]}+{m[y]}={m[x]+m[y]}")
    print(f"I2: x>y+5 -> {m[x]} > {m[y]+5}: {m[x] > m[y]+5}")
    print(f"I3: y<0 -> {m[y]}<0: {m[y] < 0}")
    print(f"I4: x%2==1 -> {m[x]}%2==1: {m[x] % 2 == 1}")
else:
    print("没有这样的model")
s.pop()