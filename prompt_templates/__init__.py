# 一阶逻辑格式要求
# fol_requirment_prompt = '''First-Order Logic Formula Requirements:
# 1.  Logical Symbols:
#     - Use `∀` for the universal quantifier
#     - Use `∃` for the existential quantifier
#     - Use `=>` for implication
# 2.  Boolean and Relational Operators: Use `!`, `&&`, `||`, `==`, `!=`, `>=`, `<=`.
# 3.  Do not use function calls in the formula except `old(x)`. All other functions, such as `max(...)`,`sum(...)`,`count(...)`, must not be used. Instead, rewrite the logic using logical connectives such as `=>`. If the function semantics cannot be expressed without calling the function, do not include the formula at all.
# 4.  Do not use ternary conditional expressions (e.g., `x ? y : z`). If needed, express the logic using implications. For example, rewrite `x ? y : z` as `(x => y) && (!x => z)`.
# 5.  Quantifiers must only be written as `∀` and `∃`. Do not use `forall` or `exists`.
# 6.  Only use quantifiers (`∀`, `∃`) when it is necessary to iterate over the elements of a data structure, such as an array. If the logic does not involve such traversal, avoid using quantifiers.
# 7.  **Whenever a quantifier (`∀` or `∃`) is used, always enclose its body in parentheses, even if it is a single expression.**  
#     - For example, write `∀ i (i >= 0)` instead of `∀ i i >= 0`.  
#     - For nested quantifiers, each quantifier body must also be enclosed in parentheses: e.g., `∀ i (∃ j (arr[i] == j))`.
# 8.  Only reference variables that appear literally in the C source (quantifier-bound variables are allowed). 
#     - Example: if the code defines a variable named `x`, the formula may use `x` (and variables like `i` introduced by `∀`/`∃`), but must NOT introduce `old_x`, `x_initial`, `x_0`, etc.
# 9.  `old(x)` can be used in loop invariants, but only when it is necessary to refer to the value of a variable outside the loop or an accumulated variable immediately before entering the current loop.
# 10. **Quantifier-bound variables must never reuse or shadow any variable already declared in the C source.**  
#     - For example, if the C code defines `i` and `sum`, you cannot write `∀ i (...)` or `∃ sum (...)`. Always choose fresh variable names for quantifiers to avoid conflicts.
# 11. When generating multiple quantifiers, each quantifier must use a fresh variable name not used elsewhere in the formula or the C code.

# Important: 
# 1. The function parameters are arbitrary, except for constraints explicitly imposed by `//@ assume()`.
# 2. The loop invariant must follow the standard definition:
#     - It holds before the first iteration.
#     - It is preserved by each iteration.
#     - Together with the loop exit condition, it implies the final assertion.    
# '''

fol_requirment_prompt = '''First-Order Logic Formula Requirements:
1.  Logical Symbols:
    - Use `∀` for the universal quantifier
    - Use `∃` for the existential quantifier
    - Use `=>` for implication
2.  Boolean and Relational Operators: Use `!`, `&&`, `||`, `==`, `!=`, `>=`, `<=`.
3.  Do not use function calls in the formula. All other functions, such as `max(...)`,`sum(...)`,`count(...)`, must not be used. Instead, rewrite the logic using logical connectives such as `=>`. If the function semantics cannot be expressed without calling the function, do not include the formula at all.
4.  Do not use ternary conditional expressions (e.g., `x ? y : z`). If needed, express the logic using implications. For example, rewrite `x ? y : z` as `(x => y) && (!x => z)`.
5.  Quantifiers must only be written as `∀` and `∃`. Do not use `forall` or `exists`.
6.  Only use quantifiers (`∀`, `∃`) when it is necessary to iterate over the elements of a data structure, such as an array. If the logic does not involve such traversal, avoid using quantifiers.
7.  **Whenever a quantifier (`∀` or `∃`) is used, always enclose its body in parentheses, even if it is a single expression.**  
    - For example, write `∀ i (i >= 0)` instead of `∀ i i >= 0`.  
    - For nested quantifiers, each quantifier body must also be enclosed in parentheses: e.g., `∀ i (∃ j (arr[i] == j))`.
8.  Only reference variables that appear literally in the C source (quantifier-bound variables are allowed). 
    - Example: if the code defines a variable named `x`, the formula may use `x` (and variables like `i` introduced by `∀`/`∃`), but must NOT introduce `old_x`, `x_initial`, `x_0`, etc.
9. **Quantifier-bound variables must never reuse or shadow any variable already declared in the C source.**  
    - For example, if the C code defines `i` and `sum`, you cannot write `∀ i (...)` or `∃ sum (...)`. Always choose fresh variable names for quantifiers to avoid conflicts.
10. When generating multiple quantifiers, each quantifier must use a fresh variable name not used elsewhere in the formula or the C code.

Important: 
1. The function parameters are arbitrary, except for constraints explicitly imposed by `//@ assume()`.
2. The loop invariant must follow the standard definition:
    - It holds before the first iteration.
    - It is preserved by each iteration.
    - Together with the loop exit condition, it implies the final assertion.    
'''

fol_requirment_prompt = '''
First-Order Logic Formula Requirements:
1.  Logical Symbols:
    - Use `∀` for the universal quantifier
    - Use `∃` for the existential quantifier
    - Use `=>` for implication
2.  Boolean and Relational Operators: Use `!`, `&&`, `||`, `==`, `!=`, `>=`, `<=`.
3.  Do not use function calls in the formula except `old(var)`. All other functions, such as `max(...)`,`sum(...)`,`count(...)`, must not be used. Instead, rewrite the logic using logical connectives such as `=>`. If the function semantics cannot be expressed without calling the function, do not include the formula at all.
4.  Do not use ternary conditional expressions (e.g., `x ? y : z`). If needed, express the logic using implications. For example, rewrite `x ? y : z` as `(x => y) && (!x => z)`.
5.  Quantifiers must only be written as `∀` and `∃`. Do not use `forall` or `exists`.
6.  Only use quantifiers (`∀`, `∃`) when it is necessary to iterate over the elements of a data structure, such as an array. If the logic does not involve such traversal, avoid using quantifiers.
7.  **Whenever a quantifier (`∀` or `∃`) is used, always enclose its body in parentheses, even if it is a single expression.**  
    - For example, write `∀ i (i >= 0)` instead of `∀ i i >= 0`.  
    - For nested quantifiers, each quantifier body must also be enclosed in parentheses: e.g., `∀ i (∃ j (arr[i] == j))`.
8.  Only reference variables that appear literally in the C source (quantifier-bound variables are allowed). 
    - Example: if the code defines a variable named `x`, the formula may use `x` (and variables like `i` introduced by `∀`/`∃`), but must NOT introduce `old_x`, `__old_x`, `x_initial`, `x_0`, `x_prev`, `x_init`, etc.
9. **Quantifier-bound variables must never reuse or shadow any variable already declared in the C source.**  
    - For example, if the C code defines `i` and `sum`, you cannot write `∀ i (...)` or `∃ sum (...)`. Always choose fresh variable names for quantifiers to avoid conflicts.
10. When generating multiple quantifiers, each quantifier must use a fresh variable name not used elsewhere in the formula or the C code.
11. `old(var)` can be used in loop invariants to refer to the value of a variable at the loop entry point (before the current iteration began).
    - **`old(var)` is the ONLY allowed syntax** for this purpose. Do NOT write `old_var`, `__old_var`, `var_old`, `var_init`, `var_prev`, or any other variant — they will cause runtime errors.
    - Example: if `sum` accumulates inside the loop, write `sum == old(sum) + j`, not `sum == old_sum + j`.

Important: 
1. The function parameters are arbitrary, except for constraints explicitly imposed by `//@ assume()`.
2. The loop invariant must follow the standard definition:
    - It holds before the first iteration.
    - It is preserved by each iteration.
    - Together with the loop exit condition, it implies the final assertion.    
'''

# 12. For known loop bounds or iteration constraints (e.g., variable bounds like `k >= 0 && k < i`), try not to embed them inside the antecedent of the implication. Instead, separate the range conditions from the implication and place them before the `=>` to ensure clear structure. This approach helps reduce the solver's solving time by making the logical formula more straightforward. Additionally, encourage using the relationship between the quantifier variable and the loop bounds rather than the iteration traversal itself. For example, write `∀ k ((k >= 0 && k < N) && (k > N/2 => a[k] == k % R))` instead of `∀ k (k >= 0 && k < i && k > N/2 => a[k] == k % R)`.





loop_code_prompt = '''Here is a piece of C language code containing some loops. 
```c
{func_code}
````

Among these loops, focus only on the code block marked with the label `TARGET_LOOP`. Its key variables are:{loop_key_vars}.
Treat any `//@ ASSUME(...)` or `//@ assume(...)` comment as a precondition constraint for the execution of the `TARGET_LOOP`. Variables without such an assumption may take arbitrary integer values at the start of the loop — their initial values are completely unknown.
Treat any `//@ assert(...)` comment as a postcondition constraint for the execution of the `TARGET_LOOP`.
Do not generate loop invariants for variables with the prefix `unknown` in their names.
'''








# task1
# task1_format_prompt = '''Please first explain your reasoning process briefly. Then, provide the final answer in the exact specified format by starting with `answer and ending with `.
# Do not include any comments, explanations, or additional text inside the answer block — only the pure JSON structure.
# Example output format:

# ```answer
# {
#     "i": ["i>=0", "i<=10", ...],
#     "j": ["j>0 && j<5", ...]
# }
# ```'''

task1_format_prompt = '''Strictly output your response as a valid JSON structure.
Do not include any other text, explanations, or formatting outside of the JSON.
Output format example:

```answer
{
    "i": ["i>=0", "i<=10"],
    "j": ["j>0 && j<5"]
}
```'''

task1_user_promot = '''For each key loop variable, generate candidate loop invariants covering:

1. **VALUE RANGES** (necessary but not sufficient):
   - Lower and upper bounds if they exist (e.g., "i >= 0", "j <= N")

2. **DATA FLOW RELATIONSHIPS** (essential for proving assertions):
   For ANY variable that is modified in the loop body (especially accumulators):
   - Identify what changes it: assignments like "var = var + expr" or "var = expr"
   - Generate invariants capturing the cumulative effect:
     * For accumulation: "var == old(var) + increment_expression"
     * For complex multi-variable relationships: "var == f(other_loop_vars)"
   - For nested loops, express inner results in terms of outer loop counters

3. **CONCRETE PATTERNS TO CONSIDER**:
   - Counter increments: if "i = i + 1" or "i++" → generate "i >= init" and "i <= bound"
   - Accumulator patterns:
     * Simple sum: "sum = sum + constant" → "sum == old(sum) + steps"
     * Weighted accumulation: "total = total + i" → "total == old(total) + sum_of_i"
     * Product/min/max: "prod = prod * i" → "prod == old(prod) * ..."
   - Multi-variable updates: "x = x + 1; y = y + x" → capture both individual and joint relationships

Generate at least 2-3 candidates per variable, including at least ONE that captures data flow (not just bounds).'''


# task1_counterexample_user_promot = '''The counterexample refers to the value of the key variables related to this loop.
# Here are some candidate loop invariants that have counterexamples.
# For any candidate that is clearly wrong under the counterexample, discard it entirely instead of returning it.
# If a candidate is too weak, strengthen it minimally so that it holds for the counterexample and remains logically sound.

# {content}'''

task1_counterexample_user_promot = '''The counterexample shows values before and after one iteration of the loop.
Here are candidate loop invariants that were found to be invalid, along with the counterexample that disproves them.

Your task:
1. **ANALYZE** the counterexample:
   - Check if the transition is mathematically possible (e.g., can "sum" go from 0 to -1 if the loop only does "sum = sum + positive"?)
   - Understand WHY each candidate failed
   - Distinguish between "the candidate formula is wrong" vs "the candidate is incomplete"

2. **LEARN** from the pattern:
   - What does this transition tell you about the variable's actual behavior?
   - If multiple candidates failed the same way, what property are they all missing?
   - Can the data flow be expressed differently?

3. **IMPROVE** your candidates:
   - If a candidate is too strong (too restrictive), relax it minimally
   - If a candidate is too weak (too permissive), strengthen it
   - If a candidate is completely wrong, replace it with a fundamentally different approach
   - If many candidates failed, try a different variable relationship pattern (e.g., if linear relationships failed, try modular relationships)
   - **Generate NEW candidates** that are consistent with this observation

4. **Data Flow Hints**:
   - For accumulators (sum, product, count): the invariant should express the relation between current value and cumulative updates
   - For loop counters: bounds should respect the loop condition
   - For multi-step updates: track the sequence of changes, not just final values

Priority: Generate at least ONE candidate that directly addresses the data flow pattern shown in the counterexample.

{content}'''



# task2
# task2_format_prompt = '''Please first explain your reasoning process briefly. Then, provide the final answer in the exact specified format by starting with ```answer and ending with ```.
# Do not include any comments, explanations, or additional text inside the answer block — only the pure JSON structure.
# Example output format:
# ```answer
# ["inv1", "inv2", ...]
# ```'''

task2_format_prompt = '''Strictly output your response as a valid JSON array.
Do not include any other text, explanations, or formatting outside of the JSON.
Output format example:

```answer
["inv1", "inv2"]
```'''


# task2_user_prompt = '''
# ## 任务
# 分析给定的循环代码，找出所有逻辑上成立的不变关系，并按以下要求组织成多个可独立验证的不变式子式。

# ## 核心要求
# 1. **自足性**：每个返回的不变式子式必须能够**单独通过霍尔逻辑验证**（初始条件成立、循环体保持）。这意味着子式内部必须包含证明其自身成立所需要的全部前提信息。
# 2. **依赖合并**：如果不变式 `B` 的证明需要另一个不变式 `A` 作为前提（例如 `B` 描述了某个变量的性质，而该变量的更新逻辑依赖于 `A` 中涉及的变量），则 **`A` 与 `B` 必须合并在同一个合取式 `A ∧ B` 中**。
# 3. **多子式输出**：返回**多个**这样的自足子式，建议 3~5 个，并按强度**从弱到强**排序（弱约束→强约束）。**不要将所有已知不变关系合并成一个单一的最强不变式**。

# ## 依赖判断指南
# - 如果某个变量的更新语句中引用了其他变量，则关于该变量的不变关系通常依赖于那些被引用变量的不变关系。
# - 条件分支（如 `if`）会使变量更新产生依赖：若某分支的更新依赖于某个条件，而该条件本身又由其他变量决定，则相关不变关系需要包含决定该条件的变量关系。

# ## 通用示例（请模仿其分层合并思路）
# 对于循环：
# ```c
# x = 0; y = 0;
# while (unknown()) {
#     x = x + 1;
#     y = y + x;
# }
# ```

# 已知可能的不变关系有：`x >= 0`, `y == x*(x-1)/2`。
# 因为 `y` 的更新使用了 `x` 的值，所以 `y == x*(x-1)/2` 的证明需要 `x` 的当前值信息，但 `x >= 0` 本身是独立的。
# 因此正确的输出是：
# ```
# [
#   "x >= 0",
#   "(x >= 0) && (y == x*(x-1)/2)"
# ]
# ```
# 而不应该是：
# ```
# ["x >= 0", "y == x*(x-1)/2"] // 第二条不能独立验证
# ```
# 也不应该是：
# ```
# ["(x >= 0) && (y == x*(x-1)/2)"] // 只输出一条，缺少弱约束子式
# ```

# '''

task2_user_prompt = '''
Generate a concise but comprehensive set of candidate loop invariants that capture meaningful relationships among key loop variables.

**Core Requirements**:
1. **Completeness**: Include invariants covering:
   - Individual variable bounds (loop counters, array indices)
   - Cumulative variable relationships (accumulators linked to loop progress)
   - Multi-variable dependencies (how one variable's update depends on others)

2. **Data Flow Focus**: For variables modified by assignments in the loop:
   - Prioritize invariants that express how the variable accumulates/changes
   - Avoid trivial bounds-only invariants if data-flow invariants exist
   - Connect accumulator variables to loop counters (e.g., "sum is proportional to loop iteration count")

3. **Quality over Quantity**:
   - Generate 3-7 distinct invariants per loop
   - Each invariant should be verifiable and logically sound
   - Avoid redundant or near-identical candidates

**Guidelines**:
- For nested loops: express inner-loop invariants that hold per iteration, and outer-loop invariants that hold after inner loop completes
- For accumulators: connect them explicitly to loop counters or iteration counts
- For conditional updates: specify conditions clearly in the invariant
- Avoid impossible contradictions (e.g., "var >= 0 && var < 0")
'''

# task2_user_prompt = '''
# Please generate a diverse but concise set of candidate loop invariants that capture meaningful value relationships among the key loop variables.

# The following variable dependencies were detected by static analysis:
# {dependency_info}

# When generating invariants, respect these dependencies. Invariants with dependencies should be generated as a single conjunctive invariant whenever possible.
# '''




# task2 带反例提问
task2_counterexample_user_promot = '''The counterexample refers to the value of the key variables related to this loop after it completes (or at a critical point).

Here are some candidate loop invariants that were disproven by a counterexample.

**Your task**:
1. **Analyze** which invariants are clearly contradictory or impossible:
   - Discard them entirely (they should NOT appear in your next response)
   - Example: if a loop only increments "i", you should never return "i < initial_value"

2. **Refine** weakened or incomplete invariants:
   - If an invariant partially holds but is missing a condition, add that condition
   - If an invariant is too restrictive, broaden it appropriately
   - Example: "sum >= 0" failed with sum = -1 → either the precondition allows negative updates, OR your assumption about sum's behavior is wrong

3. **Generate new candidates** addressing the failure:
   - Combine previously separate invariants if they are interdependent
   - Try different mathematical expressions (linear, modular, conditional)
   - Explicitly capture the cumulative nature of accumulators

4. **Data Flow Recovery**:
   - If data-flow invariants were rejected, analyze WHY the counterexample breaks them
   - Try expressing the relationship conditionally: "(phase0_pred) || (inductive_pred)"
   - Connect accumulators explicitly to loop counters and iteration counts

Return a refined set of invariants that corrects the counterexample while remaining logically sound.

{content}'''


task12_user_prompt = '''Given the key loop variables and loop context, generate candidate loop invariants. Prioritize usefulness for proving the final assertion.'''


task12_counterexample_user_prompt = '''The counterexample refers to key variable values related to this loop.
Here are candidate loop invariants that were refuted.
Discard clearly wrong formulas, and refine weak/over-strong formulas into better ones.
Regenerate a concise mixed set of candidate invariants in one pass.

{content}'''



# # task3 代码提示
# task3_loop_code_prompt = '''Here is a piece of C language code containing some loops. 
# ```c
# {func_code}
# ````

# Among these loops, focus on the code block marked with the label `{loop_name}`. Its key variables are:{loop_key_vars}.
# Treat any `//@ assume(...)` comment as a precondition constraint for the execution of the `{loop_name}`.
# Treat any `//@ assert(...)` comment as a postcondition constraint for the execution of the `{loop_name}`.
# '''

# # task3 提问

# task3_user_prompt = '''The invariant for `{loop_name}` is defined as the disjunction of the following formulas: `{invariants}`.
# This combined invariant fails to ensure the final assertion holds under the loop's postcondition.

# A counterexample was found that violates the assertion while satisfying the invariant. 
# It corresponds to the variable values after executing `{loop_name}` under the loop's postcondition.

# For any candidate that is clearly wrong under the counterexample, discard it entirely instead of returning it.
# If a candidate is too weak, strengthen it minimally so that it holds for the counterexample and remains logically sound.

# Disjunction strategy:
# Prefer invariants of the form (phase0_pred) || (inductive_pred):
# - phase0_pred describes a special initial stage before key updates (usually a literal equality check on a counter variable).
# - inductive_pred captures the long-term relation preserved in the loop.

# The counterexample is: `{counterexample_data}`.
# '''



# task3 代码提示
task3_loop_code_prompt = '''Here is a piece of C language code containing some loops. 
```c
{func_code}
````

Among these loops, focus on the code block marked with the label `TARGET_LOOP`. Its key variables are:{loop_key_vars}.
Treat any `//@ assume(...)` comment as a precondition constraint for the execution of the `TARGET_LOOP`.
Treat any `//@ assert(...)` comment as a postcondition constraint for the execution of the `TARGET_LOOP`.
'''





task3_user_prompt = '''The invariant for `TARGET_LOOP` is defined as the disjunction of the following formulas: `{invariants}`.
This combined invariant fails to ensure the final assertion holds under the loop's postcondition.

A counterexample was found that violates the assertion while satisfying the invariant. 
It corresponds to the variable values after executing `TARGET_LOOP` under the loop's postcondition.

For any candidate that is clearly wrong under the counterexample, discard it entirely instead of returning it.
If a candidate is too weak, strengthen it minimally so that it holds for the counterexample and remains logically sound.

{fail_reason}
'''



# 代码提示
task4_loop_code_prompt = '''Here is a piece of C language code containing some loops. 
```c
{func_code}
````

For each loop listed below, the loop's overall invariant is the logical AND of all formulas in its "invariants" list.
Here are the key variables and invariants of each loop:
{loop_detail}

Treat any `//@ ASSUME(...)` or `//@ assume(...)` comment as a precondition constraint.
Treat any `//@ assert(...)` comment as a postcondition constraint.
Do not generate loop invariants for variables with the prefix `unknown` in their names.
'''


# task4 带反例提问
task4_counterexample_user_promot = '''Goal: fix the loop invariants for LOOP_0 to {target_loop_name} so that verification for `{target_loop_name}` passes.

We already have candidate invariants for LOOP_0 to {target_loop_name}. But a counterexample was found when verifying loop `{ce_loop_name}`.
{ce_prompt}

You need to add new loop invariants to make verification for `{target_loop_name}` succeed..

If an inner loop invariant is too weak or incorrect, it can cause an outer loop's otherwise correct invariants to fail verification.
Therefore, review and fix **all loops from LOOP_0 up to `{target_loop_name}`**, not just the loop where the counterexample was found.
'''


task4_format_prompt = '''Strictly output your response as a valid JSON structure.
Do not include any other text, explanations, or formatting outside of the JSON.
Output format example:

```answer
{
    "LOOP_2": ["new_inv1"],
    "LOOP_3": ["new_inv2", "new_inv3"]
}
```'''