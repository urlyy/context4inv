import json
import re
from nodes.common import AgentState, clean_json, get_experiment_switches, get_true_counterexample
from langchain_core.messages import HumanMessage, AIMessage
from common import dprint
from prompt_templates import task2_counterexample_user_promot
import time

def ask_llm_for_combined_invariants_counterexample(state: AgentState, config) -> AgentState:
    llm = config["configurable"].get("llm")
    global_data = state["global_data"]
    task2_data = state["task2_data"]
    loop_data = state["loop_data"]
    
    all_counterexample = task2_data["counterexamples"]
    llm_pre_gen = task2_data["llm_gen"]
    msgs = task2_data["msgs"]

    loop_key_vars = loop_data["key_vars"]
    counterexample_vars = loop_data["counterexample_vars"]
    ssa_dicts = [loop_data["ssa_dict_after_pre"], loop_data["ssa_dict_before_loop"], loop_data["ssa_dict_after_trans"], loop_data["ssa_dict_after_loop"]]

    content = ""
    for gen_inv in llm_pre_gen:
        is_invalid = False
        reason = None
        counterexample = None
        for invalid_item in all_counterexample:
            invalid_inv = invalid_item[0]
            if invalid_inv == gen_inv:
                is_invalid = True
                reason, is_unknown, counterexample = invalid_item[1], invalid_item[2], invalid_item[3]
                break
        if not is_invalid:
            # content += f"- `{gen_inv}`. No counterexample."
            continue
        else:
            content += f"- `{gen_inv}`. "
            # dprint(counterexample)
            # dprint("==== each",invariant, key_vars, counterexample, ssa_dict_before)
            if not is_unknown:
                true_data = get_true_counterexample(gen_inv, counterexample_vars, counterexample, reason, ssa_dicts)
                content += f"A counterexample:\n{true_data}"
            else:
                content += f'The result of the Z3 solver is `unknown` due to `{counterexample}`.'
        content += "\n"
    
    
    # msg_history = state.get("messages_combined")
    # print("^"*70)
    # print(user_prompt)
    # print("^"*70)
    dprint(content)
    # content = ""
    user_prompt = task2_counterexample_user_promot.format(content=content)
    user_msg = HumanMessage(content=user_prompt)
    msgs.append(user_msg)
    msg_sent = [
        global_data["fol_msg"], 
        loop_data['loop_code_msg'],
        task2_data['format_msg'],
        user_msg,
    ]
    retry_count = get_experiment_switches(config)["task2_retry_limit"]
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
            # token_usage = response.response_metadata["token_usage"]
            # print(response.content, token_usage.get("prompt_cache_hit_tokens", token_usage.get("prompt_cache_miss_tokens")))
            cleaned_json = clean_json(response.content)
            dprint(elapsed_time)
            dprint(cleaned_json)
            gen_invariants = json.loads(cleaned_json)
            assert isinstance(gen_invariants, list)
            gen_invariants = set(gen_invariants)
            gen_ok = True
            break
        except Exception:
            if response is None:
                failed_request_count += 1
    if not gen_ok:
        # for msg in msg_sent:
        #     msg.pretty_print()
        raise Exception(f"llm_gen format error at ask_llm_for_combined_invariants_counterexample:\n{response.content if response else ''}")
    task2_data["llm_gen"] = gen_invariants
    task2_data["msgs"] = msgs
    return {
        "task2_data": task2_data,
    }
    
    # msg_history.extend([user_msg,response])
    return {"llm_gen_invariants_combined": combined_invariants, "messages_combined": msg_history}