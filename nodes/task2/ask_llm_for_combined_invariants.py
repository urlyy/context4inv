import json
import traceback
from nodes.common import AgentState, LoopNode, clean_json, get_experiment_switches
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from common import dprint
from prompt_templates import task2_format_prompt, task2_user_prompt
import time

def ask_llm_for_combined_invariants(state: AgentState, config) -> AgentState:
    llm = config["configurable"].get("llm")
    global_data = state["global_data"]
    loop_data = state["loop_data"]
    task2_data = state["task2_data"]

    msgs = task2_data["msgs"]

    path_to_loop = loop_data["path_to_loop"]
    loop_ir_node:LoopNode = path_to_loop[-1]

    print(loop_ir_node.var_deps)

    dependency_info = ""
    for var, deps in loop_ir_node.var_deps.items():
        dependency_info += f"- '{var}' depends on: {', '.join(deps)}\n"

    # true_user_prompt = task2_user_prompt.format(dependency_info=dependency_info)
    true_user_prompt = task2_user_prompt

    sys_msg_combined = SystemMessage(content=task2_format_prompt)
    user_msg = HumanMessage(content=true_user_prompt)
    msg_sent = [
        global_data["fol_msg"],
        loop_data["loop_code_msg"],
        sys_msg_combined,
        user_msg,
    ]
    msgs.append(sys_msg_combined)
    msgs.append(user_msg)
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
        # for msg in msg_sent:
        #     msg.pretty_print()
        raise Exception(f"llm_gen format error at ask_llm_for_combined_invariants:\n{response.content if response else ''}")
    task2_data["llm_gen"] = gen_invariants
    task2_data["format_msg"] = sys_msg_combined
    task2_data["msgs"] = msgs
    return {
        "task2_data": task2_data,
    }
    # messages_combined=[
    #     state["loop_sys_msg"],
    #     sys_msg_combined,
    #     user_msg,
    #     response
    # ]
    # return {
    #     "try_count_combined": 0, 
    #     "llm_gen_invariants_combined": combined_invariants, 
    #     "messages_combined": messages_combined, 
    #     "sys_msg_combined": sys_msg_combined
    # }