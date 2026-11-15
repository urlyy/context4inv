"""Preserve C source while labelling the target and verified nested loops."""

from nodes.formulas import conjoin_invariants
from nodes.ir import Loop
from nodes.state import FunctionState
from utils.c_parser import source_text


def _verified_loop_comment(
    loop_index: int, invariants: set[str], indentation: str
) -> str:
    invariant = conjoin_invariants(invariants)
    return (
        f"//@ LOOP_{loop_index} verified invariant: {invariant}\n{indentation}"
        f"// old(var) above refers to LOOP_{loop_index} entry after its initializer.\n{indentation}"
    )


def render_function_source(
    function: FunctionState,
    *,
    target_loop: Loop | None = None,
    for_prompt: bool = False,
    include_invariants: bool = True,
) -> str:
    """Annotate loop heads without removing initializers, bodies or updates.

    Loop indices follow verification order (inner loops first). Only completed
    loops receive invariant comments; each comment keeps its own old() scope.
    """
    invariants_by_loop = function["loop_invariants"]
    target_index = (
        target_loop.loop_id if target_loop is not None else len(invariants_by_loop)
    )
    syntax_node = function["syntax_node"]
    loop_indices = {
        node: index for index, node in enumerate(function["loop_syntax_nodes"])
    }
    source = syntax_node.text
    source_offset = syntax_node.start_byte
    parts = []

    def visit(node):
        if node in loop_indices:
            loop_index = loop_indices[node]
            if loop_index <= target_index:
                if loop_index < target_index and include_invariants:
                    indentation = parts[-1].rsplit("\n", 1)[-1] if parts else ""
                    parts.append(
                        _verified_loop_comment(
                            loop_index, invariants_by_loop[loop_index], indentation
                        )
                    )
                label = (
                    "TARGET_LOOP"
                    if for_prompt and loop_index == target_index
                    else f"LOOP_{loop_index}"
                )
                parts.append(label + ":")
        if node.child_count == 0:
            parts.append(source_text(node))
            return
        previous_end = node.start_byte
        for child in node.children:
            parts.append(
                source[
                    previous_end - source_offset : child.start_byte - source_offset
                ].decode("utf-8")
            )
            visit(child)
            previous_end = child.end_byte
        parts.append(
            source[previous_end - source_offset : node.end_byte - source_offset].decode(
                "utf-8"
            )
        )

    visit(syntax_node)
    return "".join(parts)
