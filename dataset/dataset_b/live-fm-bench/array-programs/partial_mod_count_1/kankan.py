from z3 import *
import json
import sys

__output_counterexample_file = None
if len(sys.argv) == 2:
    __output_counterexample_file = sys.argv[1]

__solver = Solver()

# 声明符号变量
a_0 = Array("a_0", IntSort(), IntSort())
a_1 = Array("a_1", IntSort(), IntSort())
N_0, N_1 = Ints("N_0 N_1")
i_0, i_1, i_2, i_3, i_4, i_5 = Ints("i_0 i_1 i_2 i_3 i_4 i_5")
j_0, j_1, j_2, j_3 = Ints("j_0 j_1 j_2 j_3")
R_0, R_1 = Ints("R_0 R_1")
(k_0,) = Ints("k_0")

# 声明不变式中量词的bind
{}


# 循环不变式
def INV(i, j, __old_i, __old_j):
    return And(
        j < N_1 / 2,            # 确保j始终小于N/2
        j == __old_j + 1,        # 如果a[i] == 0，则j递增
    )


# 循环前的初始化代码
PRE = And(
    N_1 == 100,
    j_1 == 0,
    R_1 == 1,
    i_1 == 0,
    And(
        ForAll(
            [k_0],
            And(
                And((k_0 >= 0), (k_0 < i_2)),
                (k_0 > (N_1 / 2)),
                (Select(a_1, k_0) == (k_0 % R_1))
            )
        ),
        (N_1 == 100),
        (R_1 == 1),
        ForAll(
            [k_0],
            And(
                (k_0 >= 0), (k_0 < i_2),
                And(
                    Implies((k_0 <= (N_1 / 2)), (Select(a_1, k_0) == (k_0 + 1))),
                    Implies((k_0 > (N_1 / 2)), (Select(a_1, k_0) == (k_0 % R_1))),
                ),
            )
        ),
        (i_2 <= N_1),
        And((i_2 >= 0), (i_2 <= N_1)),
        (i_2 >= 0),
        ForAll(
            [k_0], 
            And(
                (k_0 >= 0), 
                (k_0 < i_2), 
                (Select(a_1, k_0) >= 0),
            ),
        ),
        ForAll(
            [k_0],
            And(
                (k_0 >= 0), (k_0 < i_2),
                Or(
                    And((k_0 <= (N_1 / 2)), (Select(a_1, k_0) == (k_0 + 1))),
                    And((k_0 > (N_1 / 2)), (Select(a_1, k_0) == (k_0 % R_1))),
                )
            )
        ),
        Not((i_2 < N_1)),
    ),
    i_3 == 0,
)
# 循环条件
G = And((i_4 < N_1))
# 循环体内的变量更新
TRANS = And(
    Or(
        And(
            (Select(a_1, i_4) == 0),
            And(
                j_3 == (j_2 + 1),
            ),
        ),
        And(
            Not((Select(a_1, i_4) == 0)),
            And(
                j_3 == j_2,
            ),
        ),
    ),
    i_5 == (i_4 + 1),
)
G_EXIT = Not((i_5 < N_1))

POST = j_3 < (N_1 / 2)


def check(solver: Solver, step: int):
    if solver.check() == sat:
        if step == 0:
            print("[失败] 循环前置条件不成立！模型如下：")
        elif step == 1:
            print("[失败] 循环不变式不保持！模型如下：")
        elif step == 2:
            print("[失败] 循环后置条件不成立！模型如下：")
        model = solver.model()
        counterexample = dict()
        z3_vars = [
            a_0,
            a_1,
            N_0,
            N_1,
            i_0,
            i_1,
            i_2,
            i_3,
            i_4,
            i_5,
            j_0,
            j_1,
            j_2,
            j_3,
            R_0,
            R_1,
            k_0,
        ]
        for z3_var in z3_vars:
            counterexample[str(z3_var)] = str(model.eval(z3_var, True))

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


# === 1. 前置条件证明 ===
__solver.push()
__solver.add(
    PRE,
    Not(INV(i_3, j_1, i_3, j_1)),
)
check(__solver, 0)
__solver.pop()

# === 2. 循环不变式保持性证明 ===
__solver.push()
__solver.add(PRE, INV(i_4, j_2, i_3, j_1), G, TRANS, Not(INV(i_5, j_3, i_3, j_1)))
check(__solver, 1)
__solver.pop()

# === 3. 循环不变式后置条件证明(optional) ===
__solver.push()
__solver.add(PRE, INV(i_5, j_3, i_3, j_1), G_EXIT, Not(POST))
check(__solver, 2)
__solver.pop()

print("循环不变式成立")
