import json
import re

from nodes.common import AgentState, LoopNode, clean_json, conjuct_invariants, get_experiment_switches, get_true_counterexample
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from common import dprint, unimplement, Node, node2str
from prompt_templates import task3_loop_code_prompt, task3_user_prompt
import time

def get_new_llm_gen_invariants_post(old:list[str], extend:dict[str,list[str]], func_loops_invs:list[list[str]]):
    for loop_name, invs in extend.items():
        match = re.match(r"LOOP_(\d+)", loop_name)
        if match:
            loop_id = int(match.group(1))
            # if loop_id < len(func_loops_invs):
            #     func_loops_invs[loop_id] = invs
            # else:
            #     old.clear()
            #     old.extend(invs)
            for inv in invs:
                if loop_id < len(func_loops_invs):
                    if inv not in func_loops_invs[loop_id]:
                        func_loops_invs[loop_id].append(inv)
                elif loop_id == len(func_loops_invs):
                    if inv not in old:
                        old.append(inv)
                else:
                    pass
        else:
            # unimplement("未找到匹配")
            pass
    return 


def ask_llm_for_invariants_counterexample_post(state: AgentState, config) -> AgentState:
    llm = config["configurable"].get("llm")
    global_data = state["global_data"]
    loop_data = state["loop_data"]
    task3_data = state["task3_data"]

    loop_ir_node:LoopNode = loop_data["path_to_loop"][-1]
    
    counterexample_vars = loop_data["counterexample_vars"]
    ssa_dicts = [loop_data["ssa_dict_after_pre"], loop_data["ssa_dict_before_loop"], loop_data["ssa_dict_after_trans"], loop_data["ssa_dict_after_loop"]]

    counterexample_and_reason = task3_data["counterexample"]
    valid_invariants = task3_data["valid_invariants"]
    msgs = task3_data["msgs"]

    loop_name = f"LOOP_{loop_ir_node.loop_id}"
   
    # 构建 user_msg
    conj_invariant = conjuct_invariants(valid_invariants)
    reason, is_unknown, counterexample = counterexample_and_reason[0], counterexample_and_reason[1], counterexample_and_reason[2]
    if is_unknown:
        fail_reason = f"The result of the Z3 solver is `unknown` due to `{counterexample}`."
    else:
        true_data = get_true_counterexample(conj_invariant, counterexample_vars, counterexample, reason, ssa_dicts)
        fail_reason = f"The counterexample is:\n{true_data}"
    action = "after" if reason == 2 else "before"
    user_prompt = task3_user_prompt.format(
        loop_name=loop_name,
        invariants=valid_invariants,
        # action=action,
        fail_reason=fail_reason,
    )
    user_msg = HumanMessage(content=user_prompt)

    msgs.append(user_msg)

    msg_sent = [
        global_data["fol_msg"],
        loop_data["loop_code_msg"],
        task3_data["format_msg"],
        user_msg,
    ]
    # for msg in msg_sent:
    #     msg.pretty_print()
    retry_count = get_experiment_switches(config)["task3_retry_limit"]
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
            gen_invs = json.loads(cleaned_json)
            assert isinstance(gen_invs, list)
            gen_invs = set(gen_invs)
            gen_ok = True
            break
        except Exception:
            if response is None:
                failed_request_count += 1
    if not gen_ok:
        pass
        # for msg in msg_sent:
        #     msg.pretty_print()
        raise Exception(f"llm_gen format error at ask_llm_for_post_invariants_counterexample:\n{response.content if response else ''}")
    task3_data["llm_gen"] = gen_invs
    task3_data["msgs"] = msgs
    return {
        "task3_data": task3_data
    }