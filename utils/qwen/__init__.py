import datetime
import json
import os
import re
import sys
import time
import warnings
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough,RunnableLambda
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage,HumanMessage



os.environ["ALL_PROXY"] =''
os.environ["all_proxy"] =''
llm = ChatOpenAI(
    api_key="sk-",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    # model="qwen3-30b-a3b-instruct-2507",
    model="qwen-flash", # qwen-flash qwen3-max
)

# def new_llm(temperature):
#     return ChatOpenAI(
#         api_key="sk-19eca4b9f6c2480c92f329e17cc4e42d",
#         base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
#         # model="qwen3-30b-a3b-instruct-2507",
#         model="qwen-plus-2025-07-14",
#         temperature=temperature,
#     )

if __name__ == "__main__":
    messages = [
        AIMessage(content="Hi."),
        HumanMessage(content="Your role is a poet.Write a short poem about AI in four lines."),
    ]
    response = llm.invoke(messages)
    print(response.content)