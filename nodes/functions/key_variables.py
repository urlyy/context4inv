"""Find the variables modified by each loop, including nested loops."""

from nodes.ir import ArrayAssignment, Assignment, Conditional, Declaration, Loop
from nodes.state import WorkflowState


def _modified_variables(items, loop_variables):
    modified = set()
    for item in items:
        if isinstance(item, Declaration):
            modified.add(item.name)
        elif isinstance(item, Assignment):
            modified.add(item.target)
        elif isinstance(item, ArrayAssignment):
            modified.add(item.array_name)
        elif isinstance(item, Conditional):
            for _, body in item.branches:
                modified.update(_modified_variables(body, loop_variables))
        elif isinstance(item, Loop):
            body_variables = _modified_variables(item.body, loop_variables)
            loop_variables[item.loop_id] = sorted(body_variables)
            modified.update(body_variables)
    return modified


def find_loop_variables(state: WorkflowState) -> WorkflowState:
    function = state["function"]
    loop_variables = [[] for _ in function["loop_syntax_nodes"]]
    _modified_variables(function["statements"], loop_variables)
    function["modified_variables_by_loop"] = loop_variables
    return {"function": function}
