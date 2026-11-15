from nodes.artifacts import function_directory
from nodes.state import WorkflowState


def next_function(state: WorkflowState, config) -> WorkflowState:
    program = state["program"]
    if not program["pending_functions"]:
        return {"function": {"name": None}}
    name = program["pending_functions"].popleft()
    function_directory(config, name).mkdir()
    return {
        "program": program,
        "function": {
            "name": name,
            "syntax_node": program["function_nodes"][name],
            "loop_invariants": [],
            "modified_variables_by_loop": [],
            "ssa_states_by_loop": [],
            "counterexample_variables_by_loop": [],
        },
    }
