"""State owned by program traversal, loop traversal, and each generation stage."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import NotRequired, TypedDict

from langchain_core.messages import BaseMessage, SystemMessage
from tree_sitter import Node as SyntaxNode

from nodes.ir import Statement
from utils.c_types import CType
from utils.smt.models import CandidateRejection, LoopStateMaps, ProofFailure


class ProgramState(TypedDict):
    callers: dict[str, set[str]]
    pending_functions: deque[str]
    function_nodes: dict[str, SyntaxNode]
    formula_rules_message: SystemMessage
    function_invariants: dict[str, list[set[str]]]


class FunctionState(TypedDict):
    name: str | None
    syntax_node: SyntaxNode
    return_type: str
    statements: list[Statement]
    variable_types: dict[str, CType]
    loop_paths: list[list[Statement]]
    loop_syntax_nodes: list[SyntaxNode]
    loop_invariants: list[set[str]]
    modified_variables_by_loop: list[list[str]]
    counterexample_variables_by_loop: list[set[str]]
    ssa_states_by_loop: list[LoopStateMaps]


class LoopState(TypedDict):
    index: int
    modified_variables: list[str]
    counterexample_variables: set[str]
    path: list[Statement]
    ssa_states: LoopStateMaps
    code_message: SystemMessage


class PerVariableState(TypedDict):
    generation_round: int
    verified_invariants: dict[str, set[str]]
    candidates: dict[str, set[str]]
    has_failures: bool
    rejections: dict[str, list[CandidateRejection]]
    format_message: SystemMessage
    messages: list[BaseMessage]


class CandidateStageState(TypedDict):
    """Set-valued generation state shared by combined and joint generation."""

    generation_round: int
    verified_invariants: set[str]
    candidates: set[str]
    has_failures: bool
    rejections: list[CandidateRejection]
    format_message: SystemMessage
    messages: list[BaseMessage]


class PostconditionState(CandidateStageState):
    failure: ProofFailure
    candidate_rejections: NotRequired[dict[str, CandidateRejection]]
    invalid_candidates: NotRequired[list[str]]


@dataclass(frozen=True)
class LoopFailure:
    loop_index: int
    failure: ProofFailure


class StrengtheningState(TypedDict):
    generation_round: int
    has_failures: bool
    failure_location: LoopFailure
    candidates: dict[str, set[str]]
    format_message: SystemMessage
    messages: list[BaseMessage]
    first_modified_loop: int
    rejections_by_loop: NotRequired[dict[int, dict[str, CandidateRejection]]]
    invalid_candidates_by_loop: NotRequired[dict[int, list[str]]]


class WorkflowState(TypedDict, total=False):
    """A scope is populated by its entry node before downstream nodes read it."""

    program: ProgramState
    function: FunctionState
    loop: LoopState
    per_variable: PerVariableState
    combined: CandidateStageState
    joint: CandidateStageState
    postcondition: PostconditionState
    strengthening: StrengtheningState
