from pyparsing import (
    Word, alphas, alphanums,
    Keyword, Literal, oneOf, Suppress,
    infixNotation, opAssoc,
    Forward,
    pyparsing_common,
    ParserElement
)
ParserElement.enablePackrat() # Enable Packrat parsing for performance

# --- 1. AST Node Classes ---
class Node:
    """Base class for AST nodes for consistent __repr__."""
    def __repr__(self):
        return str(self)
    def __str__(self):
        raise NotImplementedError("Subclasses must implement __str__")

class Identifier(Node):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return str(self.name)

class Number(Node):
    def __init__(self, value):
        # pyparsing_common.number already converts to float or int
        self.value = value
    def __str__(self):
        return str(self.value)

class BooleanLiteral(Node):
    def __init__(self, value_str):
        # Store as lowercase "true" or "false"
        self.value = str(value_str).lower()
    def __str__(self):
        return self.value

class NotOp(Node):
    def __init__(self, operand):
        self.operand = operand
    def __str__(self):
        return f"Not({self.operand})"
    
class ArraySelect(Node):
    def __init__(self, array, index):
        self.array = array
        self.index = index
    def __str__(self):
        return f"Select({self.array},{self.index})"

class BinOp(Node):
    # Mapping for special logical operator string representations
    op_to_func_map = {
        "&&": "And",
        "||": "Or",
        "=>": "Implies"
    }
    # Set of operators that remain infix
    infix_operators = {"+", "-", "*", "%", "/", ">", ">=", "<", "<=", "==", "!="}

    def __init__(self, left_node, op_symbol, right_node):
        self.left = left_node
        self.op = str(op_symbol) # Ensure op_symbol is a string
        self.right = right_node

    def __str__(self):
        # Check if operator has a special function-like representation
        func_name = self.op_to_func_map.get(self.op)
        if func_name:
            return f"{func_name}({self.left},{self.right})"
        # Check if operator is a standard infix operator
        elif self.op in self.infix_operators:
            # Parenthesize infix operations to maintain structure and precedence visually
            # when they are arguments to other functions or part of complex expressions.
            return f"({self.left} {self.op} {self.right})"
        else:
            # Fallback for any unmapped operators (should not occur with this grammar)
            return f"UnknownOp({self.left}, {self.op}, {self.right})"


# --- 2. Parse Actions ---
# These functions are called when a grammar element is successfully matched.
# They convert the matched tokens (t) into an AST Node.
# s: original string, l: location, t: matched tokens
def pa_identifier(s, l, t):
    return Identifier(t[0])

def pa_number(s, l, t):
    # t[0] is already a Python int or float due to pyparsing_common.number
    return Number(t[0])

def pa_boolean_literal(s, l, t):
    return BooleanLiteral(t[0])

def pa_unary_operator(s, l, t):
    # For unary operators, t is a list of lists, e.g., [['!', operand_node]]
    op_symbol = t[0][0]
    operand_node = t[0][1]
    if op_symbol == "!":
        return NotOp(operand_node)
    # Extend here if other unary operators are added
    raise ValueError(f"Unknown unary operator symbol: {op_symbol}")

def pa_binary_operator_left_associative(s, l, t):
    # For binary operators, t is list of lists like [[left_node, op_str, right_node, op_str, next_node,...]]
    # This function handles left-associative operators.
    tokens = t[0]
    current_node = tokens[0] # First operand
    idx = 1
    while idx < len(tokens):
        op_symbol = tokens[idx]
        next_operand_node = tokens[idx+1]
        current_node = BinOp(current_node, op_symbol, next_operand_node)
        idx += 2
    return current_node

def pa_binary_operator_right_associative(s, l, t):
    # Handles right-associative operators like '=>'
    tokens = t[0]
    current_node = tokens[-1] # Start with the rightmost operand
    idx = len(tokens) - 2     # Start with the rightmost operator
    while idx > 0: # Operator index must be positive
        op_symbol = tokens[idx]
        prev_operand_node = tokens[idx-1]
        current_node = BinOp(prev_operand_node, op_symbol, current_node)
        idx -= 2
    return current_node

def pa_array_select(s, l, t):
    return ArraySelect(t[0], t[1])

# --- 3. Pyparsing Grammar Definition ---


# Base operands
identifier = Word(alphas + "_", alphanums + "_").setName("identifier")
number = pyparsing_common.number.copy().setName("number") # Handles int and float
boolean_literal = (Keyword("true") | Keyword("false")).setName("boolean_literal")

# Set parse actions for base operands
identifier.setParseAction(pa_identifier)
number.setParseAction(pa_number)
boolean_literal.setParseAction(pa_boolean_literal)

# Forward declaration for recursive expression definition
expr = Forward()

# Array support
LBRACK = Suppress("[")
RBRACK = Suppress("]")
array_ref = (identifier + LBRACK + expr + RBRACK).setParseAction(pa_array_select)

# An expression can be a base operand
base_operand = number | boolean_literal | array_ref | identifier

# Parentheses (suppressed, meaning they group but don't appear in token list for AST nodes)
LPAR = Suppress("(")
RPAR = Suppress(")")



# Operator literals
op_not = Literal("!")
op_mult_div_mod = oneOf("* / %")
op_add_sub = oneOf("+ -")
op_comparison = oneOf("> >= < <= == !=") # pyparsing handles multi-char like ">=" correctly
op_logical_and = Literal("&&")
op_logical_or = Literal("||")
op_implication = Literal("=>")

# Operator precedence and associativity definition with parse actions
# Format: (operator_literal, arity, associativity, parse_action_function)
operator_definitions_with_actions = [
    (op_not, 1, opAssoc.RIGHT, pa_unary_operator),
    (op_mult_div_mod, 2, opAssoc.LEFT, pa_binary_operator_left_associative),
    (op_add_sub, 2, opAssoc.LEFT, pa_binary_operator_left_associative),
    (op_comparison, 2, opAssoc.LEFT, pa_binary_operator_left_associative),
    (op_logical_and, 2, opAssoc.LEFT, pa_binary_operator_left_associative),  # &&
    (op_logical_or, 2, opAssoc.LEFT, pa_binary_operator_left_associative),   # ||
    (op_implication, 2, opAssoc.RIGHT, pa_binary_operator_right_associative) # =>
]

# Define the expression grammar using infixNotation
# `lpar` and `rpar` handle parenthesized expressions automatically.
expr <<= infixNotation(
    base_operand,
    operator_definitions_with_actions,
    lpar=LPAR,
    rpar=RPAR
)
        
# --- 4. Parsing Function ---
def handle_expr(expression_string):
    """
    Parses the given expression string and returns its representation
    in the specified functional/infix string format.
    """
    if not expression_string.strip():
        return "Error: Empty expression"
    # parseString returns a ParseResults object.
    # If parsing is successful and matches the whole string,
    # it will contain a single element: the root AST Node.
    result = expr.parseString(expression_string, parseAll=True)
    if result and len(result) == 1:
        root_node = result[0]
        return str(root_node) # Trigger __str__ of the root AST Node
    else:
        # This case should ideally not be reached if parseAll=True and grammar is correct
        return "Error: Malformed parse result"
    
# --- 5. 示例用法 ---
if __name__ == "__main__":
    test_expressions = [
        # "!(a+(c+d) > b && x > y || z < 5)",
        # "((a+b)*c > d+e) && (f-g < h/i)",
        # "p==1 && q>2 || !r",
        # "p==1 || q>2 && !r",
        # "a==2&&c==3 ", # Note trailing space, pyparsing handles it.
        # "a > b",
        # "!(x && y)",
        # "(e*f)+g > h || i < j",
        # "!myVar",
        # "var1 >= 100 && var2 < 50 || var3 != 0",
        # "a+b>c && b*d != (e+f)/g",
        # "(1 + 2) * 3 == 9",
        # "a", "123", "true",
        # "a && b", "c > d", "var == 20",
        # "!i && (c>d && c==20)",
        # "x || y && (z || !w)",
        # "flag", "!isActive",
        # "(a > b || x < y) && (c == 10)",
        # "a + b", "a * b + c", "a * (b + c)",
        # "i < n => k >= 0",
        # "c / 2 > 10 - 1",
        # "a+b+c", "10 - 5 * 2",
        # "val > (offset + 100) && !done",
        # "arr[0]",
        # "arr[arr[0]]",
        # "arr[x+1]",
        # "a<b==c", # Chained comparison, parsed left-associatively: ((a<b)==c)
        # "(a)", # Simple parenthesized atom
        # "!(a>b)", # Not with parenthesized expression
        # "k >= 0 && (k == 0 || (v == 0 && k % 4000 == 0) || (v == 1 && k % 2000 == 0) || (v != 0 && v != 1 && k % 10000 == 0))",
        # "a => b && c", # Implies then And (due to precedence) -> Implies(a, And(b,c))
        #               # My precedence: && is higher than =>, so (a => (b && c)) ?
        #               # Let's check: && is LEFT, => is RIGHT. && is higher precedence.
        #               # "a => b && c" is "a => (b && c)". My parser: Implies(a, And(b,c)). Correct.
        # "a && b => c", # "(a && b) => c". My parser: Implies(And(a,b), c). Correct.
        # "value + -5", # pyparsing_common.number handles "-5" as a single number token
    ]

    import time

    for i, test_expr_str in enumerate(test_expressions):
        print(f"--- 测试表达式 {i+1}: \"{test_expr_str}\" ---")
        start_time = time.perf_counter()
        formatted_string = handle_expr(test_expr_str.strip()) # Strip input
        end_time = time.perf_counter()
        duration_ms = (end_time - start_time) * 1000

        print(f"原始表达式: \"{test_expr_str}\"")
        print(f"格式化字符串: {formatted_string}")
        print(f"解析与格式化耗时: {duration_ms:.4f} ms")
        print("-" * 50)