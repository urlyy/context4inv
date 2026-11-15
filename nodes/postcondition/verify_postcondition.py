from langchain_core.messages import ToolMessage

from nodes.feedback import format_solver_diagnostic
from nodes.formulas import conjoin_invariants
from nodes.state import WorkflowState
from nodes.verification import verify_invariant


def verify_postcondition(state: WorkflowState, config):
    stage = state["postcondition"]
    loop = state["loop"]
    stage["generation_round"] += 1
    invariant = conjoin_invariants(stage["verified_invariants"])
    result = verify_invariant(
        config=config,
        invariant=invariant,
        function_name=state["function"]["name"],
        loop_index=loop["index"],
        modified_variables=loop["modified_variables"],
        symbol_names=loop["ssa_states"].exit,
        postcondition=True,
        label=f"postcondition-check-round_{stage['generation_round']}",
    )
    if result is None:
        raise ValueError(f"Invalid invariant conjunction: {invariant}")
    stage["has_failures"] = not result.valid
    diagnostic = "valid"
    if not result.valid:
        stage["failure"] = result.failure
        diagnostic = f"invalid invariants: {invariant}\n" + format_solver_diagnostic(
            invariant,
            result.failure,
            loop["counterexample_variables"],
            loop["ssa_states"],
        )
    stage["messages"].append(
        ToolMessage(
            content=diagnostic,
            tool_call_id="call_postcondition_solver",
            name="postcondition_solver",
        )
    )
    return {"postcondition": stage}
