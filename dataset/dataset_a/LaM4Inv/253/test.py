from z3 import *

x, y, z = Ints('x y z')
x1, y1, z1 = Ints('x1 y1 z1')
s = Solver()

# 看起来"合理"的不变式（但包含错误子式）
def plausible_invariant(x, y, z):
    return And(
        y == 2*x,                # I1: 正确
        z == x*(x+1)/2,          # I2: 正确
        x <= y,                  # I3: 正确
        z == y,                  # I4: 错误！
        x < 10                   # I5: 正确但弱
    )

print("=== 示例：部分错误的不变式合取 ===")

# 1. 初始验证
print("\n1. 初始验证 (x=0,y=0,z=0):")
s.push()
s.add(x == 0, y == 0, z == 0)
s.add(Not(plausible_invariant(x, y, z)))
if s.check() == unsat:
    print("   通过：初始状态满足不变式")
else:
    print("   失败：初始状态不满足不变式")
s.pop()

# 2. 迭代保持验证
print("\n2. 迭代保持验证:")
s.push()
# 迭代前满足不变式
s.add(plausible_invariant(x, y, z))
# 循环条件
s.add(x < 5)
# 循环体
s.add(x1 == x + 1)
s.add(y1 == y + 2)
s.add(z1 == z + x1)  # z 累加新的 x 值
# 验证迭代后是否仍满足
s.add(Not(plausible_invariant(x1, y1, z1)))

if s.check() == unsat:
    print("   通过：迭代中不变式保持")
else:
    print("   失败：找到反例，不变式不保持")
    m = s.model()
    print(f"   迭代前: x={m[x]}, y={m[y]}, z={m[z]}")
    print(f"   执行后: x={m.evaluate(x1)}, y={m.evaluate(y1)}, z={m.evaluate(z1)}")
    
    # 检查哪个子式被违反了
    print("\n   违反的子式检查:")
    for i, (name, cond) in enumerate([
        ("y == 2*x", y1 == 2*x1),
        ("z == x*(x+1)/2", z1 == x1*(x1+1)/2),
        ("x <= y", x1 <= y1),
        ("z == y", z1 == y1),
        ("x < 10", x1 < 10)
    ]):
        s2 = Solver()
        s2.add(x == m[x], y == m[y], z == m[z], x1 == m[x1], y1 == m[y1], z1 == m[z1])
        s2.add(Not(cond))
        if s2.check() == sat:
            print(f"      ✗ {name} 被违反")
        else:
            print(f"      ✓ {name} 保持")
s.pop()

# 3. 后置条件验证
print("\n3. 后置条件验证:")
s.push()
s.add(plausible_invariant(x, y, z))
s.add(Not(x < 5))  # 退出条件
s.add(Or(Not(y == 10), Not(z == 15)))  # 否定后置条件

if s.check() == unsat:
    print("   通过：退出时后置条件成立")
else:
    print("   失败：退出时后置条件不成立")
    m = s.model()
    print(f"   退出时: x={m[x]}, y={m[y]}, z={m[z]}")
    print(f"   期望: y=10, z=15")
s.pop()

# 4. 单独测试每个子式
print("\n4. 单独检查每个子式作为不变式的可行性:")
for name, inv in [
    ("I1: y == 2*x", lambda x,y,z: y == 2*x),
    ("I2: z == x*(x+1)/2", lambda x,y,z: z == x*(x+1)/2),
    ("I3: x <= y", lambda x,y,z: x <= y),
    ("I4: z == y", lambda x,y,z: z == y),
    ("I5: x < 10", lambda x,y,z: x < 10)
]:
    s.push()
    # 测试迭代保持
    s.add(inv(x, y, z))
    s.add(x < 5)
    x1 = x + 1
    y1 = y + 2
    z1 = z + x1
    s.add(Not(inv(x1, y1, z1)))
    if s.check() == unsat:
        print(f"   {name}: 可作为不变式")
    else:
        print(f"   {name}: 不能作为不变式")
    s.pop()