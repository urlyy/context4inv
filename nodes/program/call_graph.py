"""Collect direct function calls and schedule defined functions callee first."""

from collections import deque
from graphlib import CycleError, TopologicalSorter
from pathlib import Path

from langchain_core.messages import SystemMessage

from nodes.state import WorkflowState
from prompt_templates import fol_requirement_prompt
from utils.c_parser import init_tree, source_text


def _walk_syntax(node):
    yield node
    for child in node.named_children:
        yield from _walk_syntax(child)


def _function_name(node):
    while node.type != "identifier":
        node = node.child_by_field_name("declarator")
        if node is None:
            raise NotImplementedError("Unsupported function declarator")
    return source_text(node)


def _called_functions(function_node, declared_functions):
    callees = set()
    for node in _walk_syntax(function_node):
        if node.type != "call_expression":
            continue
        function = node.child_by_field_name("function")
        if function.type != "identifier":
            raise NotImplementedError("Indirect function calls are not supported")
        name = source_text(function)
        if name not in declared_functions:
            raise ValueError(f"Function {name!r} is not declared")
        callees.add(name)
    return callees


def analyze_program(state: WorkflowState, config) -> WorkflowState:
    source = Path(config["configurable"]["code_path"]).read_text(encoding="utf-8")
    tree, _ = init_tree(source)
    syntax_nodes = list(_walk_syntax(tree.root_node))
    declared_functions = {
        _function_name(node)
        for node in syntax_nodes
        if node.type == "function_declarator"
    }
    function_definitions = {
        _function_name(node): node
        for node in syntax_nodes
        if node.type == "function_definition"
    }
    callers = {name: set() for name in function_definitions}
    dependencies = {}
    for name in sorted(function_definitions):
        callees = _called_functions(function_definitions[name], declared_functions)
        for callee in callees:
            callers.setdefault(callee, set()).add(name)
        dependencies[name] = sorted(
            callee for callee in callees if callee in function_definitions
        )
    try:
        function_order = deque(TopologicalSorter(dependencies).static_order())
    except CycleError as error:
        raise NotImplementedError(
            "Recursive function calls are not supported"
        ) from error
    return {
        "program": {
            "callers": callers,
            "function_nodes": function_definitions,
            "pending_functions": function_order,
            "formula_rules_message": SystemMessage(content=fol_requirement_prompt),
            "function_invariants": {},
        }
    }
