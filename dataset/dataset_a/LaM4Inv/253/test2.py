from z3 import *

# 数组大小
N = 10

# 创建数组变量
A = Array('A', IntSort(), IntSort())      # 当前数组
A_orig = Array('A_orig', IntSort(), IntSort())  # 原始数组

# 其他变量
i = Int('i')
i1 = Int('i1')
A1 = Array('A1', IntSort(), IntSort())
j = Int('j')

# 量词辅助函数
def forall_range(cond, start, end):
    """创建全称量词: forall j in [start, end). cond(j)"""
    return ForAll(j, Implies(And(j >= start, j < end), cond(j)))

print("=== 示例：含量词和部分错误的不变式 ===")

# 看起来"合理"的不变式（但包含错误子式）
def plausible_invariant(i_val, A_arr):
    # I1: 0 <= i <= 5
    I1 = And(i_val >= 0, i_val <= 5)
    
    # I2: forall j. (0 <= j < i) -> A[j] == 0
    I2 = forall_range(lambda j: A_arr[j] == 0, 0, i_val)
    
    # I3: forall j. (i <= j < 10) -> A[j] >= 0
    I3 = forall_range(lambda j: A_arr[j] >= 0, i_val, N)
    
    # I4: forall j. (5 <= j < 10) -> A[j] == A_orig[j]  (错误的！)
    I4 = forall_range(lambda j: A_arr[j] == A_orig[j], 5, N)
    
    # I5: 数组总和关系（错误的！）
    # 错误假设：sum(A) == sum(A_orig) - sum(A_orig[0:i])
    # 实际上：sum(A) == sum(A_orig) - sum(A_orig[0:i]) + 0 (因为A[0:i]=0)
    # 但更严重错误：A_orig[i:10]可能不等于A[i:10]（如果i<5）
    
    # 创建求和约束（简化版，假设我们知道和函数）
    sum_A = Int('sum_A')
    sum_A_orig = Int('sum_A_orig')
    
    # 近似表示总和关系（实际应使用递归定义）
    I5 = (sum_A == sum_A_orig)  # 故意错误简化
    
    return And(I1, I2, I3, I4)

# 1. 初始验证
print("\n1. 初始验证 (i=0):")
s = Solver()

# 前置条件：所有元素非负
s.add(forall_range(lambda j: A_orig[j] >= 0, 0, N))
s.add(i == 0)
s.add(ForAll(j, A[j] == A_orig[j]))  # 初始A等于A_orig

# 检查是否满足不变式
s.add(Not(plausible_invariant(i, A)))
if s.check() == unsat:
    print("   通过：初始状态满足不变式")
else:
    print("   失败：初始状态不满足不变式")
    m = s.model()
    # 检查哪个子式被违反
    print("   违反的子式:")
    for idx, (name, cond) in enumerate([
        ("I1: 0 <= i <= 5", And(i >= 0, i <= 5)),
        ("I2: forall j<0 -> A[j]==0", BoolVal(True)),  # i=0时平凡真
        ("I3: forall j>=0 -> A[j]>=0", forall_range(lambda j: A[j] >= 0, 0, N)),
        ("I4: forall j>=5 -> A[j]==A_orig[j]", forall_range(lambda j: A[j] == A_orig[j], 5, N))
    ]):
        s2 = Solver()
        s2.add(i == m[i])
        # 复制数组约束
        for j_val in range(N):
            s2.add(A[j_val] == m.evaluate(A[j_val]))
            s2.add(A_orig[j_val] == m.evaluate(A_orig[j_val]))
        s2.add(Not(cond))
        if s2.check() == sat:
            print(f"      ✗ {name}")

# 2. 迭代保持验证
print("\n2. 迭代保持验证:")
s = Solver()

# 迭代前满足不变式
s.add(plausible_invariant(i, A))

# 循环条件
s.add(i < 5)

# 循环体
i1 = i + 1
A1 = Store(A, i, 0)  # A[i] = 0

# 验证迭代后是否仍满足
s.add(Not(plausible_invariant(i1, A1)))

if s.check() == unsat:
    print("   通过：迭代中不变式保持")
else:
    print("   失败：找到反例，不变式不保持")
    m = s.model()
    
    # 提取具体值
    i_val = m[i].as_long() if is_int_value(m[i]) else 0
    i1_val = m.evaluate(i1).as_long()
    
    print(f"   迭代前: i={i_val}")
    print(f"   执行后: i={i1_val}")
    
    # 检查A[i]的变化
    print(f"   执行前 A[{i_val}] = {m.evaluate(A[i_val])}")
    print(f"   执行后 A[{i_val}] = {m.evaluate(A1[i_val])}")
    
    # 检查哪个子式被违反
    print("\n   违反的子式检查:")
    
    # I1 检查
    s2 = Solver()
    s2.add(i == m[i], i1 == m.evaluate(i1))
    if s2.check(And(i1 >= 0, i1 <= 5)) == unsat:
        print("      ✗ I1: 0 <= i <= 5")
    
    # I4 检查（最可能错误）
    s2 = Solver()
    # 设置所有相关变量
    s2.add(i == m[i], i1 == m.evaluate(i1))
    for idx in range(N):
        s2.add(A[idx] == m.evaluate(A[idx]))
        s2.add(A_orig[idx] == m.evaluate(A_orig[idx]))
        s2.add(A1[idx] == m.evaluate(A1[idx]))
    
    # 检查 I4 在迭代后是否成立
    I4_post = forall_range(lambda j: A1[j] == A_orig[j], 5, N)
    s2.add(Not(I4_post))
    if s2.check() == sat:
        print("      ✗ I4: forall j in [5,10). A[j] == A_orig[j]")
        # 找到具体的j
        m2 = s2.model()
        j_var = Int('j')
        s3 = Solver()
        s3.add(ForAll(j_var, Implies(And(j_var >= 5, j_var < N), 
                                     A1[j_var] == A_orig[j_var])))
        s3.add(i == m[i])
        for idx in range(N):
            s3.add(A[idx] == m.evaluate(A[idx]))
            s3.add(A_orig[idx] == m.evaluate(A_orig[idx]))
            s3.add(A1[idx] == m.evaluate(A1[idx]))
        s3.check()
        # 显示反例位置
        for j in range(5, N):
            if m2.evaluate(A1[j]) != m2.evaluate(A_orig[j]):
                print(f"        位置 j={j}: A1[{j}]={m2.evaluate(A1[j])}, A_orig[{j}]={m2.evaluate(A_orig[j])}")

# 3. 展示为什么I4错误
print("\n3. I4为什么错误的演示:")
print("   I4声称: forall j. (5 <= j < 10) -> A[j] == A_orig[j]")
print("   但实际上，如果程序有bug或数组越界，A[5..9]可能被修改")
print("   更现实的情况：")
print("   - 前置条件只保证A_orig[0..9] >= 0")
print("   - 循环只修改A[0..4] = 0")
print("   - I4 假设A[5..9]从未改变，这需要额外证明")
print("   - 但如果没有相应约束，这是不可靠的假设")

# 4. 正确的修正版本
print("\n4. 正确的不变式应包含:")
print("   I1: 0 <= i <= 5")
print("   I2: forall j. (0 <= j < i) -> A[j] == 0")
print("   I3: forall j. (i <= j < 10) -> A[j] == A_orig[j]  # 关键修正！")
print("   I4: forall j. (0 <= j < 10) -> A[j] >= 0")