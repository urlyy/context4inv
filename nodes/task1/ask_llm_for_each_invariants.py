import json
import traceback
from nodes.common import AgentState, clean_json, get_experiment_switches
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from common import dprint
from prompt_templates import task1_format_prompt, task1_user_promot
import time

def ask_llm_for_each_invariants(state: AgentState, config) -> AgentState:
    llm = config["configurable"].get("llm")
    global_data = state["global_data"]
    loop_data = state["loop_data"]
    task1_data = state["task1_data"]

    loop_key_vars = loop_data["key_vars"]
    msgs = task1_data["msgs"]
    
    format_prompt_each = task1_format_prompt
    sys_msg_each = SystemMessage(content=format_prompt_each)
    user_msg = HumanMessage(content=task1_user_promot)

    msgs.append(sys_msg_each)
    msgs.append(user_msg)

    msg_sent = [
        global_data["fol_msg"],
        loop_data["loop_code_msg"],
        sys_msg_each,
        user_msg,
    ]
    retry_count = get_experiment_switches(config)["task1_retry_limit"]
    failed_request_count = 0
    gen_ok = False
    response = None
    while failed_request_count < retry_count:
        response = None
        try:
            start_time = time.perf_counter()
            response = llm.invoke(msg_sent)
            elapsed_time = time.perf_counter() - start_time
            msgs.append(response)
            cleaned_json = clean_json(response.content)
            dprint(elapsed_time)
            dprint(cleaned_json)
            gen_invariants = json.loads(cleaned_json)
            dprint(loop_key_vars)
            assert isinstance(gen_invariants, dict)
            for k in list(gen_invariants.keys()):
                if k not in loop_key_vars:
                    del gen_invariants[k]
                    continue
                v = gen_invariants[k]
                assert isinstance(v, list)
                gen_invariants[k] = set(v)
            gen_ok = True
            break
        except Exception:
            if response is None:
                failed_request_count += 1
            dprint(response.content if response else "")
            traceback.print_exc()
            
    if not gen_ok:
        # for msg in msg_sent:
        #     msg.pretty_print()
        raise Exception(f"llm_gen format error at ask_llm_for_each_invariants:\n{response.content if response else ''}")
    # messages=[
    #     state["loop_sys_msg"],
    #     sys_msg_each,
    #     user_msg,
    #     response
    # ]
    task1_data["llm_gen"] = gen_invariants
    task1_data["format_msg"] = sys_msg_each
    task1_data["msgs"] = msgs
    return {
        "task1_data": task1_data,
    }
    return {
        "try_count_each": 0, 
        "llm_gen_invariants_each": invariants, 
        "sys_msg_each": sys_msg_each,
        "messages_each": messages,
    }