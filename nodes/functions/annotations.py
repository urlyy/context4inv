"""Decode a complete verification directive from one C comment node."""

import re

from nodes.ir import Assertion, Assumption
from utils.c_parser import Node, source_text
from utils.fol_parser.parser import parse_fol


def parse_annotation(node: Node) -> Assertion | Assumption | None:
    text = source_text(node)
    line = node.start_point.row + 1
    if re.match(r"/\*\s*@", text):
        raise NotImplementedError(
            f"Block verification annotations at line {line} are not supported; use //@"
        )
    directive = re.match(r"//\s*@\s*(assume|assert)\b", text, re.IGNORECASE)
    if directive is None:
        return None
    opening = re.match(r"//\s*@\s*(assume|assert)\s*\(", text)
    if opening is None:
        raise ValueError(f"Malformed verification annotation at line {line}")
    depth = 1
    for index in range(opening.end(), len(text)):
        if text[index] == "(":
            depth += 1
        elif text[index] == ")":
            depth -= 1
        if depth != 0:
            continue
        if text[index + 1 :].strip() not in ("", ";"):
            raise ValueError(
                f"Unexpected text after verification annotation at line {line}"
            )
        expression = text[opening.end() : index].strip()
        parse_fol(expression)
        annotation_type = Assumption if opening[1] == "assume" else Assertion
        return annotation_type(expression)
    raise ValueError(f"Unbalanced annotation at line {line}")
