import json
import traceback
import time
from langchain_core.messages import HumanMessage, SystemMessage

from nodes.common import AgentState, clean_json, get_experiment_switches
from prompt_templates import task2_format_prompt, task12_user_prompt
from common import dprint


def ask_llm_for_invariants(state: AgentState, config) -> AgentState:
    llm = config["configurable"].get("llm")
    global_data = state["global_data"]
    loop_data = state["loop_data"]
    task12_data = state["task12_data"]

    msgs = task12_data["msgs"]
    sys_msg = SystemMessage(content=task2_format_prompt)
    user_msg = HumanMessage(content=task12_user_prompt)

    msg_sent = [
        global_data["fol_msg"],
        loop_data["loop_code_msg"],
        sys_msg,
        user_msg,
    ]
    msgs.append(sys_msg)
    msgs.append(user_msg)

    retry_count = get_experiment_switches(config)["task12_retry_limit"]
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
            assert isinstance(gen_invariants, list)
            gen_invariants = set(gen_invariants)
            gen_ok = True
            break
        except Exception:
            traceback.print_exc()
            if response is None:
                failed_request_count += 1

    if not gen_ok:
        raise Exception(f"llm_gen format error at ask_llm_for_invariants:\n{response.content if response else ''}")

    task12_data["llm_gen"] = gen_invariants
    task12_data["format_msg"] = sys_msg
    task12_data["msgs"] = msgs
    return {
        "task12_data": task12_data,
    }
