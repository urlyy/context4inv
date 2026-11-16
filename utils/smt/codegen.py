"""Build the initialization, preservation and optional postcondition obligations."""

from dataclasses import dataclass, replace
from pathlib import Path

from utils.fol_parser import replace_old
from utils.python_format import format_py

from .checker_template import render_checker
from .encoding import SsaEncoder, SsaState, conjunction
from .models import (
    LoopStateMaps,
    LoopVerificationInput,
    ProofPhase,
    SymbolMap,
    TemplatePaths,
)


@dataclass(frozen=True)
class PostconditionObligation:
    exit_condition: str
    transition_to_assertion: str
    assertion: str


@dataclass
class LoopProof:
    """old(var) always uses entry, including at arbitrary iteration and loop exit."""

    modified_variables: list[str]
    states: LoopStateMaps
    entry_condition: str
    iteration_condition: str
    iteration_transition: str
    postcondition: PostconditionObligation | None = None

    def invariant_at(self, symbols: SymbolMap) -> str:
        current_values = symbol_dictionary(self.modified_variables, symbols)
        entry_values = symbol_dictionary(self.modified_variables, self.states.entry)
        return f"INV({current_values}, {entry_values})"

    def definitions(self) -> str:
        lines = [
            f"PRE = {self.entry_condition}",
            f"G = {self.iteration_condition}",
            f"TRANS = {self.iteration_transition}",
        ]
        if self.postcondition is not None:
            lines.extend(
                [
                    f"POST_TRANS = {self.postcondition.transition_to_assertion}",
                    f"POST = {self.postcondition.assertion}",
                ]
            )
        return "\n".join(lines)

    def obligations(self) -> str:
        checks = [
            proof_check(
                ProofPhase.INITIALIZATION,
                [
                    "PRE",
                    f"Not({self.invariant_at(self.states.entry)})",
                ],
            ),
            proof_check(
                ProofPhase.PRESERVATION,
                [
                    "PRE",
                    self.invariant_at(self.states.before_iteration),
                    "G",
                    "TRANS",
                    f"Not({self.invariant_at(self.states.after_iteration)})",
                ],
            ),
        ]
        if self.postcondition is not None:
            checks.append(
                proof_check(
                    ProofPhase.POSTCONDITION,
                    [
                        "PRE",
                        self.invariant_at(self.states.exit),
                        self.postcondition.exit_condition,
                        "POST_TRANS",
                        "Not(POST)",
                    ],
                )
            )
        return "\n\n".join(checks)


def proof_check(phase: ProofPhase, conditions: list[str]) -> str:
    """A satisfiable negated obligation is a counterexample in this proof phase."""
    return (
        "__solver.push()\n"
        f"__solver.add({', '.join(conditions)})\n"
        f"check({int(phase)})\n"
        "__solver.pop()"
    )


def symbol_dictionary(variables: list[str], symbols: SymbolMap) -> str:
    """Keep source names in dictionary keys, outside Python's identifier namespace."""
    pairs = ", ".join(f"({name!r}, {symbols[name]})" for name in variables)
    return f"dict([{pairs}])"


def checker_source(encoder: SsaEncoder, state: SsaState, proof: LoopProof) -> str:
    # SSA symbols always end in a numeric version, unlike these fixed parameters.
    parameters = ["__current_values", "__entry_values"]
    symbols = [
        f"{name}_{version}"
        for name, final_version in state.versions.items()
        for version in range(final_version + 1)
    ]
    return render_checker(
        declarations=encoder.declarations(state),
        invariant_parameters=parameters,
        counterexample_symbols=symbols,
        definitions=proof.definitions(),
        obligations=proof.obligations(),
    )


def encode_postcondition(
    verification_input: LoopVerificationInput,
    encoder: SsaEncoder,
    loop_entry: SsaState,
    state: SsaState,
) -> PostconditionObligation:
    """Evaluate the exit guard before executing statements leading to the assertion."""
    loop = verification_input.loop
    exit_condition = f"Not({encoder.condition(loop.condition, state)})"
    transition = conjunction(encoder.encode(loop.post_statements, state))
    assertion = replace_old(
        loop.postcondition, loop_entry.versions, loop_entry.declared_variables
    )
    return PostconditionObligation(
        exit_condition=exit_condition,
        transition_to_assertion=transition,
        assertion=encoder.annotation(assertion, state),
    )


def generate_verification_templates(
    verification_input: LoopVerificationInput, paths: TemplatePaths
) -> LoopStateMaps:
    """Write candidate templates and return named SSA snapshots.

    The arbitrary iteration havocs only variables modified by the target loop.
    The exit obligation uses separate unconstrained versions, rather than assuming
    the final iteration's transition. Statements leading to the assertion never
    change the exit snapshot used to instantiate the invariant.
    """
    encoder = SsaEncoder(verification_input)
    state = SsaState.initial(verification_input.variable_types)
    entry_condition = conjunction(encoder.encode(verification_input.path[:-1], state))
    loop_entry = state.copy()

    state.havoc(verification_input.modified_variables)
    before_iteration = state.symbols
    guard = encoder.condition(verification_input.loop.condition, state)
    transition = conjunction(encoder.encode(verification_input.loop.body, state))
    states = LoopStateMaps(
        entry=loop_entry.symbols,
        before_iteration=before_iteration,
        after_iteration=state.symbols,
        exit={},
    )
    proof = LoopProof(
        modified_variables=verification_input.modified_variables,
        states=states,
        entry_condition=entry_condition,
        iteration_condition=guard,
        iteration_transition=transition,
    )
    invariant_source = checker_source(encoder, state, proof)

    if verification_input.loop.postcondition is not None:
        states = replace(states, exit=state.symbols)
        proof.states = states
        proof.postcondition = encode_postcondition(
            verification_input, encoder, loop_entry, state
        )
        write_checker_template(
            paths.postcondition, checker_source(encoder, state, proof)
        )

    write_checker_template(paths.invariant, invariant_source)
    return states


def write_checker_template(path: Path, source: str) -> None:
    path = Path(path)
    path.write_text(source, encoding="utf-8")
    diagnostic = format_py(path)
    if diagnostic is not None:
        raise ValueError(diagnostic)
