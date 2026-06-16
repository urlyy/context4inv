import json
import re
from nodes.common import AgentState, clean_json, get_experiment_switches, get_true_counterexample
from langchain_core.messages import HumanMessage, AIMessage
from common import dprint
from prompt_templates import task1_counterexample_user_promot
import time

def ask_llm_for_each_invariants_counterexample(state: AgentState, config) -> AgentState:
    llm = config["configurable"].get("llm")
    global_data = state["global_data"]
    task1_data = state["task1_data"]
    loop_data = state["loop_data"]

    all_counterexample = task1_data["counterexamples"]
    llm_pre_gen = task1_data["llm_gen"]
    msgs = task1_data["msgs"]

    loop_key_vars = loop_data["key_vars"]
    counterexample_vars = loop_data["counterexample_vars"]
    ssa_dicts = [loop_data["ssa_dict_after_pre"], loop_data["ssa_dict_before_loop"], loop_data["ssa_dict_after_trans"], loop_data["ssa_dict_after_loop"]]

    content = ""
    for key_var, gen_invs in llm_pre_gen.items():
        if key_var not in all_counterexample:
            continue
        invariants_with_reason_counterexample = all_counterexample[key_var]
        content += f"\nWrong loop invariants of the variable `{key_var}`:\n"
        for gen_inv in gen_invs:
            is_invalid = False
            reason = None
            counterexample = None
            for invalid_item in invariants_with_reason_counterexample:
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
    
    # dprint("^"*70)
    # dprint(user_prompt)
    # dprint("^"*70)
    dprint(content)
    user_prompt = task1_counterexample_user_promot.format(content=content)
    user_msg = HumanMessage(content=user_prompt)
    msgs.append(user_msg)
    msg_sent = [
        global_data["fol_msg"], 
        loop_data['loop_code_msg'],
        task1_data['format_msg'],
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
            # token_usage = response.response_metadata["token_usage"]
            # dprint(response.content, token_usage.get("prompt_cache_hit_tokens", token_usage.get("prompt_cache_miss_tokens")))
            cleaned_json = clean_json(response.content)
            dprint(elapsed_time)
            dprint(cleaned_json)
            gen_invariants = json.loads(cleaned_json)
            assert isinstance(gen_invariants, dict)
            for key_var in list(gen_invariants.keys()):
                if key_var not in loop_key_vars:
                    del gen_invariants[key_var]
                    continue
                invariants = gen_invariants[key_var]
                assert isinstance(invariants, list)
                gen_invariants[key_var] = set(invariants)
            gen_ok = True
            break
        except Exception:
            if response is None:
                failed_request_count += 1
    if not gen_ok:
        # for msg in msg_sent:
        #     msg.pretty_print()
        raise Exception(f"llm_gen format error at ask_llm_for_each_invariants_counterexample:\n{response.content if response else ''}")
    
    task1_data["llm_gen"] = gen_invariants
    task1_data["msgs"] = msgs

    return {
        "task1_data": task1_data,
    }
    
    # msg_history.extend([user_msg,response])
    
    # return {"llm_gen_invariants_each": gen_invariants, "messages_each": msg_history}