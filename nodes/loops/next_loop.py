"""Advance loop analysis and prepare the source context shown to the model."""

from langchain_core.messages import SystemMessage

from nodes.artifacts import (
    create_loop_artifacts,
    function_directory,
    loop_directory,
    loop_source_path,
)
from nodes.ir import ArrayAssignment, Assignment, Conditional, Loop
from nodes.source_rendering import render_function_source
from nodes.state import WorkflowState
from prompt_templates import loop_code_prompt
from utils.expr_parser.ast import free_variable_names
from utils.expr_parser.parser import parse_expression


def find_counterexample_variables(statements, variable_names):
    variables = set()

    def condition_variables(condition):
        return free_variable_names(parse_expression(condition)) & set(variable_names)

    for statement in statements:
        if isinstance(statement, Assignment):
            variables.add(statement.target)
        elif isinstance(statement, ArrayAssignment):
            variables.add(statement.array_name)
            variables.update(condition_variables(statement.index))
        elif isinstance(statement, Conditional):
            for condition, branch in statement.branches:
                variables.update(condition_variables(condition))
                variables.update(find_counterexample_variables(branch, variable_names))
        elif isinstance(statement, Loop):
            variables.update(condition_variables(statement.condition))
            variables.update(
                find_counterexample_variables(statement.body, variable_names)
            )
    return variables


def _loop_context(function, loop, modified_variables):
    source = render_function_source(function, target_loop=loop, for_prompt=True)
    message = SystemMessage(
        content=loop_code_prompt.format(
            func_code=source,
            loop_key_vars=",".join(f"`{name}`" for name in modified_variables),
        )
    )
    return source, message


def next_loop(state: WorkflowState, config) -> WorkflowState:
    function = state["function"]
    loop_index = state["loop"]["index"] + 1
    function_name = function["name"]
    if loop_index == len(function["loop_paths"]):
        source = render_function_source(function)
        (function_directory(config, function_name) / "FINAL_code.c").write_text(
            source, encoding="utf-8"
        )
        return {"loop": {"index": loop_index}}

    path = function["loop_paths"][loop_index]
    loop = path[-1]
    create_loop_artifacts(
        config,
        function_name,
        loop_index,
        has_postcondition=loop.postcondition is not None,
    )
    modified_variables = function["modified_variables_by_loop"][loop_index]
    counterexample_variables = find_counterexample_variables(
        loop.body, function["variable_types"]
    )
    function["counterexample_variables_by_loop"].append(counterexample_variables)
    source, message = _loop_context(function, loop, modified_variables)
    loop_source_path(config, function_name, loop_index).write_text(
        source, encoding="utf-8"
    )
    (
        loop_directory(config, function_name, loop_index) / "pre_code_prompt.log"
    ).write_text(message.pretty_repr(), encoding="utf-8")
    return {
        "function": function,
        "loop": {
            "index": loop_index,
            "modified_variables": modified_variables,
            "path": path,
            "code_message": message,
            "counterexample_variables": counterexample_variables,
        },
    }
