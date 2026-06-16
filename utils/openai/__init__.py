import os
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage,HumanMessage


# os.environ["ALL_PROXY"] =''
# os.environ["all_proxy"] =''
llm = ChatOpenAI(
    api_key="sk-",
    base_url="https://openrouter.ai/api/v1",
    model="openai/gpt-5",
    extra_body={
        "provider": {
             "only": ["openai"]
        },
    }
)

if __name__ == "__main__":
    messages = [
        AIMessage(content="Hi."),
        HumanMessage(content="Your role is a poet.Write a short poem about AI in four lines."),
    ]
    response = llm.invoke(messages)
    print(response.content)