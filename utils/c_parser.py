"""C syntax trees using the prebuilt Tree-sitter grammar."""

import tree_sitter_c
from tree_sitter import Language, Node, Parser, Tree

from utils.expr_parser.ast import Variable, walk_expression
from utils.expr_parser.parser import parse_expression

__all__ = [
    "C_LANGUAGE",
    "Language",
    "Node",
    "Tree",
    "init_tree",
    "source_text",
    "identifiers_in_expression",
]

C_LANGUAGE = Language(tree_sitter_c.language())


def init_tree(code: str) -> tuple[Tree, Language]:
    """Parse one source file and reject syntax errors before building verification IR."""
    tree = Parser(C_LANGUAGE).parse(code.encode("utf-8"))
    if tree.root_node.has_error:
        raise ValueError("C source contains syntax errors")
    return tree, C_LANGUAGE


def source_text(node: Node) -> str:
    """Decode the exact source span belonging to a Tree-sitter node."""
    return node.text.decode("utf-8")


def identifiers_in_expression(expression: str) -> list[str]:
    """Extract source identifiers for dependency analysis, retaining their order."""
    tree = parse_expression(expression)
    return list(
        dict.fromkeys(
            node.name for node in walk_expression(tree) if isinstance(node, Variable)
        )
    )
