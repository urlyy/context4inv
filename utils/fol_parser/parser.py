# -*- coding: utf-8 -*-
from pyparsing import (
    Word, alphas, alphanums,
    Keyword, Literal, oneOf, Suppress,
    infixNotation, opAssoc,
    Forward, Group, OneOrMore,
    pyparsing_common,
    ParserElement,delimitedList
)
ParserElement.enablePackrat() # Enable Packrat parsing for performance

quantifier_binder_var_set = None

# --- 1. AST Node Classes (MODIFIED) ---
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
        self.value = value
    def __str__(self):
        return str(self.value)

class BooleanLiteral(Node):
    def __init__(self, value_str):
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
    op_to_func_map = { "&&": "And", "||": "Or", "=>": "Implies" }
    infix_operators = {"+", "-", "*", "%", "/", ">", ">=", "<", "<=", "==", "!="}

    def __init__(self, left_node, op_symbol, right_node):
        self.left = left_node
        self.op = str(op_symbol)
        self.right = right_node

    def __str__(self):
        func_name = self.op_to_func_map.get(self.op)
        if func_name:
            return f"{func_name}({self.left},{self.right})"
        elif self.op in self.infix_operators:
            return f"({self.left} {self.op} {self.right})"
        else:
            return f"UnknownOp({self.left}, {self.op}, {self.right})"

# MODIFIED: AST Nodes for Quantifiers to accept a list of variables
class ForAll(Node):
    def __init__(self, variables, body):
        self.variables = variables # Now a list
        self.body = body
    def __str__(self):
        var_str = ", ".join(map(str, self.variables))
        return f"ForAll([{var_str}], {self.body})"

class Exists(Node):
    def __init__(self, variables, body):
        self.variables = variables # Now a list
        self.body = body
    def __str__(self):
        var_str = ", ".join(map(str, self.variables))
        return f"Exists([{var_str}], {self.body})"

# --- 2. Parse Actions (MODIFIED) ---
def pa_identifier(s, l, t):
    return Identifier(t[0])

def pa_number(s, l, t):
    return Number(t[0])

def pa_boolean_literal(s, l, t):
    return BooleanLiteral(t[0])

def pa_unary_operator(s, l, t):
    op_symbol, operand_node = t[0]
    if op_symbol == "!":
        return NotOp(operand_node)
    elif op_symbol == "-":
        return BinOp(Number(0), "-", operand_node)
    raise ValueError(f"Unknown unary operator symbol: {op_symbol}")

def pa_binary_operator_left_associative(s, l, t):
    tokens = t[0]
    node = tokens[0]
    for i in range(1, len(tokens), 2):
        op, operand = tokens[i], tokens[i+1]
        node = BinOp(node, op, operand)
    return node

def pa_binary_operator_right_associative(s, l, t):
    tokens = t[0]
    node = tokens[-1]
    for i in range(len(tokens) - 2, 0, -2):
        op, operand = tokens[i], tokens[i-1]
        node = BinOp(operand, op, node)
    return node

def pa_array_select(s, l, t):
    return ArraySelect(t[0], t[1])

# MODIFIED: Parse Action for Quantifiers to handle lists and flexible structure
def pa_quantifier(s, l, t):
    quant_symbol = t[0]
    # Tokens can be [symbol, [vars], body] or [symbol, [[vars], body]]
    # Flattening simplifies access
    flat_tokens = t.asList()
    variable_nodes = flat_tokens[1]
    body_node = flat_tokens[2]

    for var_node in variable_nodes:
        quantifier_binder_var_set.add(var_node.name)
    
    if quant_symbol == '∀':
        return ForAll(variable_nodes, body_node)
    elif quant_symbol == '∃':
        return Exists(variable_nodes, body_node)
    raise ValueError(f"Unknown quantifier symbol: {quant_symbol}")

def pa_comparison_chain(s, l, t):
    tokens = t[0]
    # 例如 tokens = [0, '<=', k, '<', i]
    if len(tokens) > 3:
        clauses = []
        for i in range(1, len(tokens), 2):
            left, op, right = tokens[i-1], tokens[i], tokens[i+1]
            clauses.append(BinOp(left, op, right))
        # 把多个比较用 And 串起来
        node = clauses[0]
        for c in clauses[1:]:
            node = BinOp(node, "&&", c)
        return node
    else:
        return BinOp(tokens[0], tokens[1], tokens[2])


# --- 3. Pyparsing Grammar Definition (MODIFIED) ---
# Forward declare the top-level grammar for recursion
final_grammar = Forward()

# Base operands
identifier = Word(alphas + "_", alphanums + "_").setParseAction(pa_identifier)
number = pyparsing_common.number.copy().setParseAction(pa_number)
boolean_literal = (Keyword("true") | Keyword("false")).setParseAction(pa_boolean_literal)

# Infix expression grammar (the part without top-level quantifiers)
infix_expr = Forward()
LBRACK, RBRACK = Suppress("["), Suppress("]")
array_ref = (identifier + LBRACK + infix_expr + RBRACK).setParseAction(pa_array_select)
LPAR, RPAR = Suppress("("), Suppress(")")
op_not, op_mult_div_mod, op_add_sub, op_comparison, op_logical_and, op_logical_or, op_implication = \
    Literal("!"), oneOf("* / %"), oneOf("+ -"), oneOf("> >= < <= == !="), Literal("&&"), Literal("||"), Literal("=>")

operator_definitions = [
    ((op_not | Literal("-")), 1, opAssoc.RIGHT, pa_unary_operator),
    (op_mult_div_mod, 2, opAssoc.LEFT, pa_binary_operator_left_associative),
    (op_add_sub, 2, opAssoc.LEFT, pa_binary_operator_left_associative),
     (op_comparison, 2, opAssoc.LEFT, pa_comparison_chain),
    (op_logical_and, 2, opAssoc.LEFT, pa_binary_operator_left_associative),
    (op_logical_or, 2, opAssoc.LEFT, pa_binary_operator_left_associative),
    (op_implication, 2, opAssoc.RIGHT, pa_binary_operator_right_associative)
]


# Grammar for Quantifiers
op_forall, op_exists = Literal("∀"), Literal("∃")
# Capture one or more identifiers for multi-variable quantifiers
quant_vars = Group(delimitedList(identifier))

# A quantifier can have a parenthesized body OR a semicolon-separated body
# CRITICAL: The body is now `final_grammar` to allow for nesting.
quant_body_paren = LPAR + final_grammar + RPAR
quant_body_semicolon = Suppress(";") + final_grammar
quantified_expr = Forward()
quantified_expr <<= ((op_forall | op_exists) + quant_vars + (quantified_expr | quant_body_paren | quant_body_semicolon)
                    ).setParseAction(pa_quantifier)

base_operand = number | boolean_literal | array_ref | identifier | quantified_expr

infix_expr <<= infixNotation(base_operand, operator_definitions, lpar=LPAR, rpar=RPAR)



final_grammar <<= infix_expr

def remove_redundant_parentheses(expr_str):
    """Remove redundant parentheses from the expression string"""
    stack = []
    pairs = []
    
    # Find all matching parentheses
    for i, char in enumerate(expr_str):
        if char == '(':
            stack.append(i)
        elif char == ')':
            if stack:
                start = stack.pop()
                pairs.append((start, i))
    
    # Identify redundant parentheses
    to_remove = set()
    for start, end in pairs:
        # Check if these parentheses are redundant
        substr = expr_str[start+1:end]
        
        # Count parentheses balance in substring
        balance = 0
        has_outer_operator = False
        for char in substr:
            if char == '(':
                balance += 1
            elif char == ')':
                balance -= 1
            elif balance == 0 and char in ['&', '|', '=', '>', '<', '!', '+', '-', '*', '/', '%']:
                has_outer_operator = True
                break
        
        # If no outer operator and balanced parentheses, these are redundant
        if not has_outer_operator and balance == 0:
            to_remove.add(start)
            to_remove.add(end)
    
    # Build new string without redundant parentheses
    result = ''.join(char for i, char in enumerate(expr_str) if i not in to_remove)
    return result

# --- 4. Parsing Function ---
def fol_to_z3(expression_string):
    if not expression_string.strip():
        raise Exception("Error: Empty fol")
    try:
        expression_string = remove_redundant_parentheses(expression_string)
        global quantifier_binder_var_set
        quantifier_binder_var_set = set()
        result = final_grammar.parseString(expression_string, parseAll=True)
        return str(result[0]), quantifier_binder_var_set
    except Exception as e:
        # e.args = (f"{e.args[0]}\nillegal fol: {expression_string}",)
        raise Exception(f"{e.args[0]}\nillegal fol: {expression_string}")
        

# --- 5. 示例用法 ---
if __name__ == "__main__":
    test_expressions = [
        "((i > 0) => (∀ m (0 <= m && m < i => (∀ n (m + 1 <= n && n < len => s[m] != s[n]) || (∃ p (m + 1 <= p && p < len && s[m] == s[p] && (result == m || result > m)))))))",
        "(i > 0) => (∀ m (0 <= m && m < i => (∀ n (m + 1 <= n && n < len => s[m] != s[n]) || (∃ p (m + 1 <= p && p < len && s[m] == s[p] && (result == m || result > m))))))"
    ]


     

    # for i, test_expr_str in enumerate(test_expressions):
    #     print(f"--- Testing Expression {i+1} ---")
    #     print(f"Original:   \"{test_expr_str}\"")
    #     formatted_string = fol_to_z3(test_expr_str.strip())
    #     print(f"Formatted:  {formatted_string}")
    #     print("-" * 50)


    test_cases = [
        ("(∀ m (0 <= m && m < i))", "∀ m (0 <= m && m < i)"),
        ("((i>0) => (c==0))", "((i>0) => (c==0))"),
         ("a > 0 && ((i>0) => (c==0))", "a > 0 && ((i>0) => (c==0))"),
          ("a > 0 || ((a==0) && (i>0) => (c==0))", "a > 0 || ((a==0) && (i>0) => (c==0))"),
    ]

    for data, expected in test_cases:
        res = remove_redundant_parentheses(data)
        print(res)
        assert(res == expected)


 # "!(a+(c+d) > b && x > y || z < 5)",
        # "((a+b)*c > d+e) && (f-g < h/i)",
        # "p==1 && q>2 || !r",
        # "arr[x+1]", "a < b == c",
        # "k >= 0 && (k == 0 || (v == 0 && k % 4000 == 0))",
        # "a => b && c",
        # "∀k (k > 0)",
        # "∃j (arr[j] == value)",
        # # --- THE FAILING CASES ---
        # "∃i ∃j; 0 <= i && i < j && j < n && a[i] == a[j]",
        # "∀i (i > 0 => i+1 > i)",
        # "∀i (∃j (arr[i] == j))",
        # # --- END FAILING CASES ---
        # "∃x (!(x > 100 || x < 0))",
        # "∀k (k >= 0 && k < size => arr[k] > 0)",
        # "(k == n_0) => ∀m(j_1 <= m && m < n_0)",
        # "∀j (0 <= j && j < n) => ∃k (j <= k && k <= n)",
        # "∃j1,j2((0 <= j1 && j1 <= i) && (0 <= j2 && j2 <= i) && (j1 + j2 <= i))",
        # "k == -j",
        # "∀aa((0 < aa && aa <= j) => (k == -aa))",
        # "a==Max(1,2)"
        # "(∀i (i >= 0 && i < n) => a[i] == b[i]) == (result == 1) && (∃i (i >= 0 && i < n) && a[i] != b[i]) == (result == 0)"
        # "∀k(0 <= k < i => max >= a[k])",
        # "∀k((0 <= k && k <= j) => (a_0[k] <= a_0[j]))",
        # "∀ j (j >= 0 && j < i => a[j] == 1)",
        # "sum[0] == i && i >= 0",
        # "∀ k1 ∀ k2 (k1 >= 0 && k1 < i && k2 >= 0 && k2 < i && k1 != k2 => a[k1] != a[k2] || (k1 % 3 == k2 % 3))"
        # "∀k ((0 <= k && k < i) => (a[k] == 8 * (k + 1)))",