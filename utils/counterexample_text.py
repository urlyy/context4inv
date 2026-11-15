"""Optional human-readable descriptions of Z3 array models."""

from langchain_core.messages import HumanMessage

PROMPT_TEMPLATE = """Given a Z3 array expression using K, Store, or Lambda, describe it in one short sentence:
- K(Int, X) → default value X
- Store(array, i, v) → A[i]=v
- Lambda(x, expr) → describe rule as "A[i] = expr"
For complex conditions, summarize with a simple rule or pattern, ignore details.
Example: Lambda(x, x*2) → "Array where A[i] = i*2"
Input: {}
Output:"""


def z3_model_to_nl(array_expr: str, llm) -> str:
    """Ask the injected model for a display description; never use it as proof evidence."""
    prompt = PROMPT_TEMPLATE.format(array_expr)
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content
