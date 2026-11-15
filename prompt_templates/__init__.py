"""Prompts for candidate generation and counterexample refinement."""

fol_requirement_prompt = """
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
11. `old(var)` is the variable's value at entry to the loop whose invariant you are generating, after that loop's initializer and before its first guard check. It is fixed across that loop's iterations.
    - **`old(var)` is the ONLY allowed syntax** for this purpose. Do NOT write `old_var`, `__old_var`, `var_old`, `var_init`, `var_prev`, or any other variant — they will cause runtime errors.
    - In an inner-loop invariant, `old(var)` refers to that invocation of the inner loop, not the enclosing loop or function entry. It already includes effects of earlier outer-loop iterations.

Important:
1. The function parameters are arbitrary, except for constraints explicitly imposed by `//@ assume()`.
2. The loop invariant must follow the standard definition:
    - It is checked at the loop head, after the target loop's initializer and before every guard check, including the first check.
    - It is preserved by the complete iteration, including the for-loop update, on return to that same loop head.
    - Together with the loop exit condition, it implies the final assertion.
    - At an enclosing loop's head, an inner for-loop's initializer has not run for the new enclosing iteration. Do not assume the inner counter already represents current inner-loop progress there; a local not initialized on the incoming path may have any value.
"""

loop_code_prompt = """Here is a piece of C language code containing some loops.
```c
{func_code}
````

Among these loops, focus only on the code block marked with the label `TARGET_LOOP`. Its key variables are:{loop_key_vars}.
The source retains every loop's initializer, body and update. Comments labelled `LOOP_n verified invariant` belong only to that labelled loop; `old(var)` in such a comment is bound to that loop's own entry.
Respect explicit assignments and `//@ assume(...)` constraints on the path to `TARGET_LOOP`. At an arbitrary enclosing-loop iteration, its guard and verified invariants constrain the state; do not assume its initialization still describes every variable.
Treat any `//@ assert(...)` comment as a postcondition constraint for the execution of the `TARGET_LOOP`.
Do not generate loop invariants for variables with the prefix `unknown` in their names.
"""

per_variable_format_prompt = """Strictly output your response as a valid JSON structure.
Do not include any other text, explanations, or formatting outside of the JSON.
Output format example:

```answer
{
    "i": ["i>=0", "i<=10"],
    "j": ["j>0 && j<5"]
}
```"""

per_variable_generation_prompt = """For each key loop variable, generate candidate loop invariants covering:

1. **VALUE RANGES** (necessary but not sufficient):
   - Lower and upper bounds if they exist (e.g., "i >= 0", "j <= N")

2. **DATA FLOW RELATIONSHIPS** (essential for proving assertions):
   For ANY variable that is modified in the loop body (especially accumulators):
   - Identify what changes it: assignments like "var = var + expr" or "var = expr"
   - Generate invariants capturing the cumulative effect:
     * For accumulation: relate the current value to its loop-entry value and cumulative progress since that same entry.
     * For complex multi-variable relationships: "var == f(other_loop_vars)"
   - For nested loops, keep entry snapshots local to each loop. An inner loop's `old(var)` already includes earlier outer-loop work; do not add that work again.

3. **CONCRETE PATTERNS TO CONSIDER**:
   - Counter increments: if "i = i + 1" or "i++" → generate "i >= init" and "i <= bound"
   - Accumulator patterns:
     * Simple sum: "sum = sum + constant" → "sum == old(sum) + steps"
     * Weighted accumulation: "total = total + i" → "total == old(total) + sum_of_i"
     * Product/min/max: "prod = prod * i" → "prod == old(prod) * ..."
   - Multi-variable updates: "x = x + 1; y = y + x" → capture both individual and joint relationships

Generate at least 2-3 candidates per variable, including at least ONE that captures data flow (not just bounds)."""

per_variable_refinement_prompt = """Use the table headers to identify whether verification failed at loop entry or across one iteration.
If a `value_at_loop_entry (old)` column is present, it gives the fixed values used by `old(var)`; these can differ from values immediately before the displayed iteration.
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

{content}"""

list_format_prompt = """Strictly output your response as a valid JSON array.
Do not include any other text, explanations, or formatting outside of the JSON.
Output format example:

```answer
["inv1", "inv2"]
```"""

combined_generation_prompt = """
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
"""

combined_refinement_prompt = """Use the table headers to distinguish loop-entry values from values before and after one iteration.
The `value_at_loop_entry (old)` column, when present, gives the fixed values used by `old(var)`.

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

{content}"""

joint_generation_prompt = """Given the key loop variables and loop context, generate candidate loop invariants. Prioritize usefulness for proving the final assertion."""

joint_refinement_prompt = """The counterexample refers to key variable values related to this loop.
Here are candidate loop invariants that were refuted.
Discard clearly wrong formulas, and refine weak/over-strong formulas into better ones.
Regenerate a concise mixed set of candidate invariants in one pass.

{content}"""

postcondition_refinement_prompt = """The verified invariant for `TARGET_LOOP` is the conjunction of: `{invariants}`.
Verification has not proved the final assertion. The diagnostic below is either a concrete counterexample or an `unknown` result.

Keep the verified formulas unchanged. Generate additional inductive constraints that, together with them and the loop exit condition, imply the assertion.
For an exit counterexample, exclude the unreachable bad state while retaining all reachable states. Do not try to make the new constraint hold in that bad state.
Every new constraint must hold at loop entry and be preserved by the loop body. An `unknown` result is inconclusive; prefer equivalent solver-friendly formulas without claiming that the solver found a counterexample.
Return only the additional candidate constraints in the required JSON format.

{fail_reason}
"""

strengthening_code_prompt = """Here is a piece of C language code containing some loops.
```c
{func_code}
````

For each loop listed below, the loop's overall invariant is the logical AND of all formulas in its "invariants" list.
Every `old(var)` in a loop's list refers to that labelled loop's own entry after its initializer. The snapshots for different loops are distinct, even when they mention the same variable.
Here are the key variables and invariants of each loop:
{loop_detail}

Treat any `//@ ASSUME(...)` or `//@ assume(...)` comment as a precondition constraint.
Treat any `//@ assert(...)` comment as a postcondition constraint.
Do not generate loop invariants for variables with the prefix `unknown` in their names.
"""

strengthening_refinement_prompt = """Goal: fix the loop invariants for LOOP_0 to {target_loop_name} so that verification for `{target_loop_name}` passes.

We already have candidate invariants for LOOP_0 to {target_loop_name}. But a counterexample was found when verifying loop `{ce_loop_name}`.
{ce_prompt}

You need to add new loop invariants to make verification for `{target_loop_name}` succeed..

If an inner loop invariant is too weak or incorrect, it can cause an outer loop's otherwise correct invariants to fail verification.
Therefore, review and fix **all loops from LOOP_0 up to `{target_loop_name}`**, not just the loop where the counterexample was found.
"""

strengthening_format_prompt = """Strictly output your response as a valid JSON structure.
Do not include any other text, explanations, or formatting outside of the JSON.
Output format example:

```answer
{
    "LOOP_2": ["new_inv1"],
    "LOOP_3": ["new_inv2", "new_inv3"]
}
```"""
