from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import HumanMessage, SystemMessage

token = "sk-"

llm = ChatDeepSeek(
    model="deepseek-chat",
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=token,
    # temperature=
)

def get_balance():
    import requests

    url = "https://api.deepseek.com/user/balance"

    payload={}
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)


if __name__  == "__main__":
    get_balance()
    exit()
    s1 = '''
    我给你一个python函数，函数代码如下:
    def f(x):
        a = 1
        b = 3
        c = 4
        d = 6
        xx = 555
        e = 5
        return x + 1
    你将会根据此函数，回答问题。
    '''
    # from utils.compute_token import compute_token
    # token_num = compute_token(s1)
    # print(token_num)
    msg = [
        SystemMessage(s1),
        HumanMessage("向f传入5,结果是多少?"),
    ]

    resp = llm.invoke(msg)
    print(resp)

    # msg = [
    #     SystemMessage(s1),
    #     HumanMessage("向f传入6,结果是多少?只需要返回答案。不需要返回其他信息。"),
    # ]

    # resp = llm.invoke(msg)
    # print(resp)

    # '''
    # 输出如下
    # 68
    # content='6' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 1, 'prompt_tokens': 88, 'total_tokens': 89, 'completion_tokens_details': None, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}, 'prompt_cache_hit_tokens': 0, 'prompt_cache_miss_tokens': 88}, 'model_name': 'deepseek-chat', 'system_fingerprint': 'fp_8802369eaa_prod0425fp8', 'id': 'aaca278a-1a03-40d6-b9a0-fa991fcfa943', 'service_tier': None, 'finish_reason': 'stop', 'logprobs': None} id='run--9abaf310-94d9-423f-b69b-b4e6a188aea5-0' usage_metadata={'input_tokens': 88, 'output_tokens': 1, 'total_tokens': 89, 'input_token_details': {'cache_read': 0}, 'output_token_details': {}}
    # content='7' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 1, 'prompt_tokens': 88, 'total_tokens': 89, 'completion_tokens_details': None, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 64}, 'prompt_cache_hit_tokens': 64, 'prompt_cache_miss_tokens': 24}, 'model_name': 'deepseek-chat', 'system_fingerprint': 'fp_8802369eaa_prod0425fp8', 'id': 'da1d0111-1d18-4b5a-8ac5-119c6a303751', 'service_tier': None, 'finish_reason': 'stop', 'logprobs': None} id='run--4b00e994-b927-442c-949a-3f5204b9325f-0' usage_metadata={'input_tokens': 88, 'output_tokens': 1, 'total_tokens': 89, 'input_token_details': {'cache_read': 64}, 'output_token_details': {}}
    
    # 可以看到cache_read:64, 即system_message被缓存了
    # 具体参考: https://api-docs.deepseek.com/zh-cn/guides/kv_cache
    # '''

    