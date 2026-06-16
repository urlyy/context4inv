import os
from langchain_community.chat_models import ChatZhipuAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

os.environ["ZHIPUAI_API_KEY"] = ""

llm = ChatZhipuAI(
    model="glm-4-flash-250414",
    temperature=0.5,
)

# messages = [
#     AIMessage(content="Hi."),
#     HumanMessage(content="Your role is a poet.Write a short poem about AI in four lines."),
# ]
# response = llm.invoke(messages)
# print(response.content)

# from langchain_core.messages import HumanMessage
    
# prompt_template = '''Given a Z3 array expression using K, Store, or Lambda, describe it in one short sentence:
# - K(Int, X) → default value X
# - Store(array, i, v) → A[i]=v
# - Lambda(x, expr) → describe rule as "A[i] = expr"
# For complex conditions, summarize with a simple rule or pattern, ignore details.
# Example: Lambda(x, x*2) → "Array where A[i] = i*2"
# Input: {}
# Output:'''


# def z3_model_to_nl(array_expr: str) -> str:
#     prompt = prompt_template.format(array_expr)
#     response = llm.invoke([HumanMessage(content=prompt)])
#     return response.content


# if __name__ == "__main__":
#     test_cases = [
#         "K(Int, 3)",
#         "Lambda(k!0,\n       If(Or(And(0 <= k!0, 1 <= k!0),\n             And(0 <= k!0, Not(1 <= k!0))),\n          3,\n          6))",
#         "Store(Store(Store(Store(K(Int, 7), 1, 20), 3, 123), 0, 10),5,30)"
#     ]
    
#     for i, expr in enumerate(test_cases, 1):
#         print(f"Origin: {repr(expr)}")
#         result = z3_model_to_nl(expr)
#         print(f"After:  {repr(result)}")
#         print()