from z3 import *

def example_one_at_a_time():
    print("=== 例子 1: 反例的片面性 ===")
    
    # 1. 定义变量
    x = Int('x')
    x_prime = Int('x_prime')

    # 2. 定义候选不变式 (Candidates)
    # h1: x < 10  (显然错)
    # h2: x < 50  (也是错的，但在 x=10 时还没错)
    # h3: x <= 100 (正确)
    h1 = x < 10
    h2 = x < 50
    h3 = x <= 100
    
    candidates = {"h1": h1, "h2": h2, "h3": h3}
    
    # 对应的“下一状态”候选式 (把 x 换成 x_prime)
    h1_prime = x_prime < 10
    h2_prime = x_prime < 50
    h3_prime = x_prime <= 100
    
    candidates_prime = {"h1": h1_prime, "h2": h2_prime, "h3": h3_prime}

    # 3. 构造 SMT 求解器
    s = Solver()

    # 4. 添加 Houdini 验证逻辑: 
    # {Current_Inv} Guard & Body {Current_Inv}
    # 我们寻找反例，即： Pre holds AND Guard holds AND Trans holds AND (Post Fails)
    
    # A. 归纳假设 (Inductive Hypothesis): 假设当前所有候选都成立
    s.add(And(h1, h2, h3))
    
    # B. 循环守卫 (Guard): x < 100
    s.add(x < 100)
    
    # C. 状态转移 (Transition): x' = x + 1
    s.add(x_prime == x + 1)
    
    # D. 否定后置条件: 只要有一个候选在下一步失效，就是反例
    s.add(Not(And(h1_prime, h2_prime, h3_prime)))

    # 5. 求解
    if s.check() == sat:
        m = s.model()
        print(f"[Z3 找到反例]: x = {m[x]}, x_prime = {m[x_prime]}")
        print("-" * 30)
        
        # 6. 【关键步骤】利用这个模型，批量验证谁挂了
        print("正在利用反例进行批量验证...")
        valid_count = 0
        for name, expr_prime in candidates_prime.items():
            # evaluate 返回 True/False
            is_hold = m.evaluate(expr_prime) 
            
            if is_hold:
                print(f"❌ 漏网之鱼: [{name}] 验证通过 (True)。它依然留在池子里！")
            else:
                print(f"✅ 成功捕获: [{name}] 验证失败 (False)。剔除！")
                
        print("-" * 30)
        print("结论：你看，h2 (x < 50) 明明是错的，但在 x=10 这个反例下，")
        print("它被判定为'通过'。如果你不跑下一轮，你就把它当成真理了。")
        
    else:
        print("没有找到反例 (Unsat)")

if __name__ == "__main__":
    example_one_at_a_time()