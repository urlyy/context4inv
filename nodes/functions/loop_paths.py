"""Build a verification path to every loop in postorder."""

from nodes.ir import BranchCondition, Conditional, EnclosingLoopCondition, Loop
from nodes.state import WorkflowState


def _visible_dependencies(dependencies):
    """Leave source-variable relationships useful in the loop prompt."""
    visible = {}
    for name, related_variables in dependencies.items():
        if name.startswith("unknown"):
            continue
        related = set()
        for variable in related_variables:
            if variable != name and not variable.startswith("unknown"):
                related.add(variable)
        if related:
            visible[name] = related
    return visible


def find_loop_paths(state: WorkflowState) -> WorkflowState:
    function = state["function"]
    paths = []

    def visit(items, prefix):
        preceding = []
        for item in items:
            if isinstance(item, Loop):
                paths.append(prefix + preceding + [item])
                item.variable_dependencies = _visible_dependencies(
                    item.variable_dependencies
                )
                visit(
                    item.body,
                    prefix
                    + preceding
                    + [EnclosingLoopCondition(item.condition, item.loop_id)],
                )
            elif isinstance(item, Conditional):
                for condition, body in item.branches:
                    visit(body, prefix + preceding + [BranchCondition(condition)])
            preceding.append(item)

    visit(function["statements"], [])
    function["loop_paths"] = sorted(paths, key=lambda path: path[-1].loop_id)
    return {"function": function}
