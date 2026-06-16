import json
import re
import traceback
from nodes.common import AgentState, clean_json, get_true_counterexample, get_current_code, conjuct_invariants, get_experiment_switches
from langchain_core.messages import HumanMessage, SystemMessage
from common import dprint
from prompt_templates import task4_counterexample_user_promot, task4_loop_code_prompt
import time

# 问当前循环的
def ask_llm_for_invariants_counterexample(state: AgentState, config) -> AgentState:
    llm = config["configurable"].get("llm")
    global_data = state["global_data"]
    func_data  = state["func_data"]
    loop_data = state["loop_data"]
    task4_data = state["task4_data"]

    func_name = func_data["cur_name"]
    func_node = func_data["cur_node"]
    loop_nodes = func_data["loop_nodes"]
    loops_invs = func_data["loops_invs"]
    loops_key_vars = func_data["loops_key_vars"]

    msgs = task4_data["msgs"]

    path_to_loops = func_data["path_to_loops"]
    loop_ir_nodes = []
    for p in path_to_loops:
        ir_node = p[-1]
        loop_ir_nodes.append(ir_node)

    code = get_current_code(
        config,
        func_name,
        func_node,
        None,
        loop_nodes,
        loop_ir_nodes,
        loops_invs,
        False,
        add_inv_comment=False,
        write_file=False,
    )
    loop_detail = ""
    for loop_id, key_vars in enumerate(loops_key_vars):
        detail = {
            "key_variables": list(key_vars),
            "invariants": list(loops_invs[loop_id])
        }
        loop_detail += f'''- LOOP_{loop_id}: {detail}\n'''

    code_msg = SystemMessage(content=task4_loop_code_prompt.format(
        func_code=code,
        loop_detail=loop_detail
    ))

    # tmp = {k: v for k, v in task4_data.items() if k not in ('format_msg', 'msgs')}
    # dprint(tmp)

    ce_reason_data, ce_loop_id = task4_data["ce_and_loop_id"]
    ssa_dicts = func_data["loops_ssa_dicts"][ce_loop_id]
    counterexample_vars = func_data["loops_counterexample_vars"][ce_loop_id]
    ce_reason, ce_is_unknown, ce_data = ce_reason_data
    dprint(ce_loop_id)
    ce_loop_invs = loops_invs[ce_loop_id]
    conj_loop = conjuct_invariants(ce_loop_invs)
    action = "after" if ce_reason == 2 else "before"
    ce_loop_name=f"LOOP_{ce_loop_id}"
    if ce_is_unknown:
        true_data = get_true_counterexample(conj_loop, counterexample_vars, ce_data, ce_reason, ssa_dicts)
        ce_prompt = f'''The counterexample is the concrete variable values immediately {action} `{ce_loop_name}`:\n{true_data}'''
    else:
        ce_prompt = f'''The result of the Z3 solver is "unknown" immediately {action} `{ce_loop_name}` due to `{ce_data}`'''
    user_prompt = task4_counterexample_user_promot.format(
        ce_loop_name=ce_loop_name,
        ce_prompt=ce_prompt,
        action=action,
        target_loop_name=f"LOOP_{loop_data['cur_id']}",
    )
    user_msg = HumanMessage(content=user_prompt)
    # code_msg.pretty_print()
    # user_msg.pretty_print()
    msgs.append(code_msg)
    msgs.append(user_msg)
    msg_sent = [
        global_data["fol_msg"], 
        code_msg,
        user_msg,
        task4_data['format_msg'],
    ]
    retry_count = get_experiment_switches(config)["task4_retry_limit"]
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
            response.pretty_print()
            # token_usage = response.response_metadata["token_usage"]
            # print(response.content, token_usage.get("prompt_cache_hit_tokens", token_usage.get("prompt_cache_miss_tokens")))
            cleaned_json = clean_json(response.content)
            dprint(elapsed_time)
            dprint(cleaned_json)
            gen_invariants:dict[str,list[str]] = json.loads(cleaned_json)
            assert isinstance(gen_invariants, dict)
            for k, v in gen_invariants.items():
                assert isinstance(v, list)
            gen_ok = True
            break
        except Exception:
            traceback.print_exc()
            if response is None:
                failed_request_count += 1
    if not gen_ok:
        # for msg in msg_sent:
        #     msg.pretty_print()
        raise Exception(f"llm_gen format error at ask_llm_for_invariants_counterexample:\n{response.content if response else ''}")
    
    smallest_modified_loop_id = None
    for loop_name, new_invs in gen_invariants.items():
        modified_loop_id = int(loop_name.split("_")[-1])
        if smallest_modified_loop_id:
            smallest_modified_loop_id = min(smallest_modified_loop_id, modified_loop_id)
        else:
            smallest_modified_loop_id = modified_loop_id
    # func_data["loops_invs"] = loops_invs
    task4_data["msgs"] = msgs
    task4_data["smallest_modified_loop_id"] = smallest_modified_loop_id
    task4_data["try_count"] += 1
    task4_data["llm_gen"] = gen_invariants
    return {
        "func_data": func_data,
        "task4_data": task4_data,
    }