from nodes.common import AgentState, get_func_subject_dir



def next_func(state: AgentState, config) -> AgentState:
    global_data = state["global_data"]
    q = global_data["func_to_visit_queue"]
    func_data = state["func_data"]
    if len(q) == 0:
        func_data["cur_name"] = None
        return {
            "func_data": func_data
        }
    
    cur_handled_func_name = q.popleft()
    global_data["func_to_visit_queue"] = q

    get_func_subject_dir(config, cur_handled_func_name, True)
    
    func_data["cur_name"] = cur_handled_func_name
    cur_func_node = global_data["func_node_dict"][cur_handled_func_name]
    func_data["cur_node"] = cur_func_node

    return {
        "global_data": global_data,
        "func_data": func_data
    }