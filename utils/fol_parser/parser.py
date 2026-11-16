"""Parse annotations once, then render their AST directly as Z3 source."""

from utils.expr_parser.ast import Expression
from utils.expr_parser.parser import make_grammar, parse_expression
from utils.expr_parser.rendering import Z3Renderer

_FOL_EXPRESSION = make_grammar(quantified=True)


def parse_fol(expression: str | Expression) -> Expression:
    """Accept an existing AST so old(expr) resolution never reparses source."""
    if isinstance(expression, Expression):
        return expression
    return parse_expression(expression, _FOL_EXPRESSION)


def fol_to_z3(expression, variable_names=None, *, bound_prefix=""):
    """Compile free-variable substitutions with separate, scoped quantifier symbols."""
    tree = parse_fol(expression)
    renderer = Z3Renderer(variable_names, bound_prefix=bound_prefix)
    code = renderer.render(tree)
    return code, renderer.quantified_symbols
