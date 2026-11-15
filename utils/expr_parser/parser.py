"""Parse C expressions and first-order annotations into the shared syntax tree."""

from threading import RLock

from pyparsing import (
    Forward,
    Group,
    Keyword,
    Literal,
    ParseBaseException,
    ParserElement,
    Regex,
    Suppress,
    Word,
    alphanums,
    alphas,
    delimited_list,
    infix_notation,
    one_of,
    opAssoc,
)

from .ast import (
    ArrayAccess,
    BinaryExpression,
    BooleanLiteral,
    NumberLiteral,
    OldExpression,
    Quantifier,
    UnaryExpression,
    Variable,
)
from .rendering import Z3Renderer

ParserElement.enable_packrat()
_PARSE_LOCK = RLock()


def left_associative_operator(tokens, *, c_semantics):
    operands = tokens[0]
    expression = operands[0]
    for index in range(1, len(operands), 2):
        expression = BinaryExpression(
            expression, operands[index], operands[index + 1], c_semantics
        )
    return expression


def right_associative_operator(tokens, *, c_semantics):
    operands = tokens[0]
    expression = operands[-1]
    for index in range(len(operands) - 2, 0, -2):
        expression = BinaryExpression(
            operands[index - 1], operands[index], expression, c_semantics
        )
    return expression


def mathematical_comparison_chain(tokens):
    """Annotations read 0 <= i < n as a conjunction; C keeps C precedence."""
    operands = tokens[0]
    clauses = [
        BinaryExpression(operands[index - 1], operands[index], operands[index + 1])
        for index in range(1, len(operands), 2)
    ]
    expression = clauses[0]
    for clause in clauses[1:]:
        expression = BinaryExpression(expression, "&&", clause)
    return expression


def make_grammar(*, quantified=False):
    """Annotations add quantifiers, old(expr), and mathematical comparison chains."""
    expression = Forward()
    identifier = Word(alphas + "_", alphanums + "_").set_parse_action(
        lambda tokens: Variable(tokens[0])
    )
    number = Regex(r"(?:\d+\.\d*|\.\d+|\d+)(?:[eE][+-]?\d+)?").set_parse_action(
        lambda tokens: NumberLiteral(tokens[0])
    )
    boolean = (Keyword("true") | Keyword("false")).set_parse_action(
        lambda tokens: BooleanLiteral(tokens[0] == "true")
    )

    def array_access(tokens):
        array = tokens[0]
        for index in tokens[1:]:
            array = ArrayAccess(array, index, c_semantics=not quantified)
        return array

    array = identifier + (Suppress("[") + expression + Suppress("]"))[1, ...]
    array.set_parse_action(array_access)
    operand = number | boolean | array | identifier
    if quantified:
        old_expression = (
            Keyword("old").suppress() + Suppress("(") + expression + Suppress(")")
        ).set_parse_action(lambda tokens: OldExpression(tokens[0]))
        operand = old_expression | operand

        quantifier = Forward()
        variables = Group(delimited_list(identifier))
        body = (
            quantifier
            | (Suppress("(") + expression + Suppress(")"))
            | (Suppress(";") + expression)
        )
        quantifier <<= (one_of("∀ ∃") + variables + body).set_parse_action(
            lambda tokens: Quantifier(tokens[0], tuple(tokens[1]), tokens[2])
        )
        operand |= quantifier

    def left_binary(tokens):
        return left_associative_operator(tokens, c_semantics=not quantified)

    def right_binary(tokens):
        return right_associative_operator(tokens, c_semantics=not quantified)

    comparisons = (
        [(one_of("< <= > >= == !="), 2, opAssoc.LEFT, mathematical_comparison_chain)]
        if quantified
        else [
            (one_of("< <= > >="), 2, opAssoc.LEFT, left_binary),
            (one_of("== !="), 2, opAssoc.LEFT, left_binary),
        ]
    )
    expression <<= infix_notation(
        operand,
        [
            (
                one_of("! + -"),
                1,
                opAssoc.RIGHT,
                lambda tokens: UnaryExpression(
                    tokens[0][0], tokens[0][1], not quantified
                ),
            ),
            (one_of("* / %"), 2, opAssoc.LEFT, left_binary),
            (one_of("+ -"), 2, opAssoc.LEFT, left_binary),
            *comparisons,
            (Literal("&&"), 2, opAssoc.LEFT, left_binary),
            (Literal("||"), 2, opAssoc.LEFT, left_binary),
            (Literal("=>"), 2, opAssoc.RIGHT, right_binary),
        ],
    )
    return expression


_C_EXPRESSION = make_grammar()


def parse_expression(source, grammar=_C_EXPRESSION):
    if not source.strip():
        raise ValueError("Empty expression")
    try:
        # pyparsing resets a process-wide packrat cache for each parse.
        with _PARSE_LOCK:
            return grammar.parse_string(source, parse_all=True)[0]
    except ParseBaseException as error:
        raise ValueError(f"Invalid expression: {source}\n{error}") from error


def handle_expr(source, variable_names=None) -> str:
    """Compile a C expression; the checker supplies C scalar-conversion helpers."""
    return Z3Renderer(variable_names).render(parse_expression(source))
