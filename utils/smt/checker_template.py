"""Self-contained Python checker source; candidate placeholders stay named.

The runtime is copied into each artifact so a saved checker can run independently
of the project's imports. Exit statuses distinguish a proof failure, unknown,
and candidate construction errors from ordinary Python execution failures.
"""

from string import Template

from .models import SOLVER_TIMEOUT_SECONDS
from .protocol import COUNTEREXAMPLE_EXIT, INVALID_INVARIANT_EXIT, UNKNOWN_EXIT

CHECKER_TEMPLATE = Template("""from z3 import *
import json
import sys

__solver = Solver()
__solver.set(timeout=$solver_timeout_ms)
__output = sys.argv[1] if len(sys.argv) == 2 else None

def __as_bool(value):
    return value if is_bool(value) else value != 0

def __as_number(value):
    return If(value, IntVal(1), IntVal(0)) if is_bool(value) else value

def __to_int(value):
    value = __as_number(value)
    if is_real(value):
        return If(value >= 0, ToInt(value), -ToInt(-value))
    return value

$declarations

# Variables bound in the candidate invariant:
{candidate_bindings}
# Candidate invariant: {candidate_description}
def INV($invariant_parameters):
    try:
        candidate = {candidate_expression}
        if not is_bool(candidate):
            raise TypeError("An invariant must be a Boolean expression")
        return candidate
    except (NameError, TypeError, ValueError, Z3Exception) as error:
        if __output:
            with open(__output, "w", encoding="utf-8") as stream:
                json.dump(dict(kind="invalid_invariant", error_type=type(error).__name__,
                               message=str(error)), stream, ensure_ascii=False)
        sys.exit($invalid_invariant_exit)

$definitions

def check(step):
    result = __solver.check()
    if result == unsat:
        return
    data = dict(reason=step)
    if result == unknown:
        data["unknown_reason"] = __solver.reason_unknown()
        status = $unknown_exit
    else:
        model = __solver.model()
        data["counterexample"] = dict(
            (str(symbol), str(model.eval(symbol, model_completion=True)))
            for symbol in [$counterexample_symbols]
        )
        status = $counterexample_exit
    if __output:
        with open(__output, "w", encoding="utf-8") as stream:
            json.dump(data, stream, ensure_ascii=False)
    sys.exit(status)

$obligations
""")


def render_checker(
    *,
    declarations,
    invariant_parameters,
    counterexample_symbols,
    definitions,
    obligations,
):
    """Reserve 10% of the process budget for imports and writing a solver result."""
    return CHECKER_TEMPLATE.substitute(
        declarations=declarations,
        invariant_parameters=", ".join(invariant_parameters),
        counterexample_symbols=", ".join(counterexample_symbols),
        definitions=definitions,
        obligations=obligations,
        solver_timeout_ms=max(1, int(SOLVER_TIMEOUT_SECONDS * 900)),
        counterexample_exit=COUNTEREXAMPLE_EXIT,
        unknown_exit=UNKNOWN_EXIT,
        invalid_invariant_exit=INVALID_INVARIANT_EXIT,
    )
