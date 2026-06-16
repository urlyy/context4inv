import json
import time
from langchain_core.messages import HumanMessage

from nodes.common import AgentState, clean_json, get_experiment_switches, get_true_counterexample
from prompt_templates import task12_counterexample_user_prompt
from common import dprint


def ask_llm_for_invariants_counterexample(state: AgentState, config) -> AgentState:
    llm = config["configurable"].get("llm")
    global_data = state["global_data"]
    task12_data = state["task12_data"]
    loop_data = state["loop_data"]

    all_counterexample = task12_data["counterexamples"]
    llm_pre_gen = task12_data["llm_gen"]
    msgs = task12_data["msgs"]

    counterexample_vars = loop_data["counterexample_vars"]
    ssa_dicts = [
        loop_data["ssa_dict_after_pre"],
        loop_data["ssa_dict_before_loop"],
        loop_data["ssa_dict_after_trans"],
        loop_data["ssa_dict_after_loop"],
    ]

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
            continue

        content += f"- `{gen_inv}`. "
        if not is_unknown:
            true_data = get_true_counterexample(gen_inv, counterexample_vars, counterexample, reason, ssa_dicts)
            content += f"A counterexample:\n{true_data}"
        else:
            content += f"The result of the Z3 solver is `unknown` due to `{counterexample}`."
        content += "\n"

    dprint(content)
    user_prompt = task12_counterexample_user_prompt.format(content=content)
    user_msg = HumanMessage(content=user_prompt)
    msgs.append(user_msg)
    msg_sent = [
        global_data["fol_msg"],
        loop_data["loop_code_msg"],
        task12_data["format_msg"],
        user_msg,
    ]

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
            if response is None:
                failed_request_count += 1

    if not gen_ok:
        raise Exception(f"llm_gen format error at ask_llm_for_invariants_counterexample:\n{response.content if response else ''}")

    task12_data["llm_gen"] = gen_invariants
    task12_data["msgs"] = msgs
    return {
        "task12_data": task12_data,
    }
