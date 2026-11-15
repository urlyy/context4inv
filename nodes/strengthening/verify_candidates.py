"""Rebuild summaries in order and check every loop affected by strengthening."""

from itertools import count

from langchain_core.messages import ToolMessage

from nodes.artifacts import invariant_template_path, postcondition_template_path
from nodes.config import read_experiment_options
from nodes.feedback import (
    format_candidate_rejections,
    format_solver_diagnostic,
    remember_rejections,
)
from nodes.formulas import conjoin_invariants
from nodes.state import LoopFailure, WorkflowState
from nodes.verification import verify_candidate_set, verify_invariant
from utils.smt import generate_verification_templates
from utils.smt.models import LoopVerificationInput, TemplatePaths


def _refresh_templates(function, loop_index, config):
    verification = LoopVerificationInput(
        path=function["loop_paths"][loop_index],
        variable_types=function["variable_types"],
        loop_invariants=function["loop_invariants"],
        modified_variables_by_loop=function["modified_variables_by_loop"],
    )
    paths = TemplatePaths(
        invariant=invariant_template_path(config, function["name"], loop_index),
        postcondition=postcondition_template_path(config, function["name"], loop_index),
    )
    states = generate_verification_templates(verification, paths)
    function["ssa_states_by_loop"][loop_index] = states
    return states


def _verify_additions(function, stage, loop_index, states, config):
    accepted = function["loop_invariants"][loop_index]
    modified_variables = function["modified_variables_by_loop"][loop_index]
    candidates = set(stage["candidates"].get(f"LOOP_{loop_index}", ()))
    generated = set(candidates)
    candidate_numbers = count(1)

    def verify(candidate, verified):
        return verify_invariant(
            config=config,
            invariant=conjoin_invariants(verified | {candidate}),
            function_name=function["name"],
            loop_index=loop_index,
            modified_variables=modified_variables,
            symbol_names=states.before_iteration,
            label=f"strengthening-round_{stage['generation_round']}-loop_{loop_index}-idx_{next(candidate_numbers)}",
        )

    rejected = verify_candidate_set(
        candidates,
        accepted,
        verify,
        fixed_point=read_experiment_options(config).fixed_point_enabled,
    )
    remembered = stage.setdefault("rejections_by_loop", {}).setdefault(loop_index, {})
    remember_rejections(remembered, rejected, accepted)
    invalid_by_loop = stage.setdefault("invalid_candidates_by_loop", {})
    invalid = set(invalid_by_loop.get(loop_index, ())) | (generated - candidates)
    invalid_by_loop[loop_index] = sorted(invalid - accepted)
    return format_candidate_rejections(
        rejected,
        generated - candidates,
        f"LOOP_{loop_index}",
        function["counterexample_variables_by_loop"][loop_index],
        states,
    )


def _verify_loop_conjunction(function, stage, loop_index, states, config):
    loop = function["loop_paths"][loop_index][-1]
    has_postcondition = loop.postcondition is not None
    invariant = conjoin_invariants(function["loop_invariants"][loop_index])
    result = verify_invariant(
        config=config,
        invariant=invariant,
        function_name=function["name"],
        loop_index=loop_index,
        modified_variables=function["modified_variables_by_loop"][loop_index],
        symbol_names=states.exit if has_postcondition else states.before_iteration,
        postcondition=has_postcondition,
        label=f"strengthening-conjunction-round_{stage['generation_round']}-loop_{loop_index}",
    )
    if result is None:
        raise ValueError(
            f"Invalid invariant conjunction for {function['name']}-LOOP_{loop_index}"
        )
    return result


def verify_candidates(state: WorkflowState, config):
    function = state["function"]
    stage = state["strengthening"]
    stage["has_failures"] = False
    messages = []
    for loop_index in range(stage["first_modified_loop"], state["loop"]["index"] + 1):
        states = _refresh_templates(function, loop_index, config)
        messages.append(_verify_additions(function, stage, loop_index, states, config))
        result = _verify_loop_conjunction(function, stage, loop_index, states, config)
        if result.valid:
            messages.append(f"LOOP_{loop_index}: valid")
            continue
        stage["has_failures"] = True
        stage["failure_location"] = LoopFailure(loop_index, result.failure)
        messages.append(
            f"LOOP_{loop_index}: "
            + format_solver_diagnostic(
                conjoin_invariants(function["loop_invariants"][loop_index]),
                result.failure,
                function["counterexample_variables_by_loop"][loop_index],
                states,
            )
        )
        break
    stage["messages"].append(
        ToolMessage(
            content="\n".join(message for message in messages if message),
            tool_call_id="call_strengthening_solver",
            name="strengthening_solver",
        )
    )
    return {"strengthening": stage, "function": function}
