"""Translate the supported C statement subset into verification IR."""

from nodes.functions.annotations import parse_annotation
from nodes.ir import (
    ArrayAssignment,
    Assertion,
    Assignment,
    Conditional,
    Declaration,
    Loop,
    Parameter,
    Statement,
)
from nodes.state import WorkflowState
from utils.c_parser import Node, identifiers_in_expression, source_text
from utils.c_types import VAR_POINTER, CType


def variable_dependencies(items: list[Statement]) -> dict[str, set[str]]:
    dependencies = {}
    for item in items:
        if isinstance(item, Declaration):
            dependencies.setdefault(item.name, set())
        elif isinstance(item, (Assignment, ArrayAssignment)):
            name = item.target if isinstance(item, Assignment) else item.array_name
            values = set(identifiers_in_expression(item.value))
            if isinstance(item, ArrayAssignment):
                values.update(identifiers_in_expression(item.index))
            dependencies.setdefault(name, set()).update(values)
        elif isinstance(item, Conditional):
            for condition, body in item.branches:
                for name, values in variable_dependencies(body).items():
                    dependencies.setdefault(name, set()).update(
                        values | set(identifiers_in_expression(condition))
                    )
        elif isinstance(item, Loop):
            for name, values in item.variable_dependencies.items():
                dependencies.setdefault(name, set()).update(values)
    return dependencies


class FunctionParser:
    def __init__(self):
        self.variable_types: dict[str, CType] = {}
        self.loop_syntax_nodes: list[Node] = []
        self.array_parameters: set[str] = set()

    @staticmethod
    def _unsupported(node: Node, detail: str = ""):
        line, column = node.start_point
        suffix = f": {detail}" if detail else ""
        raise NotImplementedError(
            f"Unsupported C {node.type} at {line + 1}:{column + 1}{suffix}"
        )

    def read_pure_expression(self, node: Node) -> str:
        """Expressions embedded in a statement must have no side effects."""
        if node.type in (
            "assignment_expression",
            "update_expression",
            "call_expression",
            "pointer_expression",
        ):
            self._unsupported(node, "side effects/pointer operations in expressions")
        for child in node.named_children:
            self.read_pure_expression(child)
        return source_text(node)

    def _scalar_type_name(self, node: Node):
        type_node = node.child_by_field_name("type")
        type_name = source_text(type_node)
        if type_node.type not in ("primitive_type", "sized_type_specifier"):
            self._unsupported(node, "only scalar and one-dimensional array types")
        # As in the verifier, integer arithmetic uses mathematical integers.
        if type_name in ("signed", "signed int", "unsigned", "unsigned int"):
            type_name = "int"
        if type_name not in ("int", "long", "float", "double"):
            self._unsupported(node, f"type {type_name!r}")
        return type_name

    def parse_declaration(self, node: Node, parameter=False) -> list[Statement]:
        for child in node.named_children:
            if child.type == "storage_class_specifier" and source_text(child) in (
                "static",
                "extern",
                "_Thread_local",
                "thread_local",
            ):
                self._unsupported(child, "non-automatic storage duration")
        declarators = node.children_by_field_name("declarator")
        if (
            parameter
            and source_text(node.child_by_field_name("type")) == "void"
            and not declarators
        ):
            return []
        type_name = self._scalar_type_name(node)
        statements = []
        for declarator in declarators:
            statements.extend(
                self._parse_declarator(declarator, type_name, parameter=parameter)
            )
        return statements

    def _parse_declarator(self, declarator: Node, type_name: str, *, parameter: bool):
        initializer = None
        if declarator.type == "init_declarator":
            initializer = declarator.child_by_field_name("value")
            declarator = declarator.child_by_field_name("declarator")
        is_array = declarator.type in ("array_declarator", "pointer_declarator")
        if declarator.type == "array_declarator":
            size = declarator.child_by_field_name("size")
            if size is not None:
                self.read_pure_expression(size)
        name_node = (
            declarator.child_by_field_name("declarator") if is_array else declarator
        )
        if name_node.type != "identifier":
            self._unsupported(declarator, "nested declarator")
        name = source_text(name_node)
        if name in self.variable_types:
            self._unsupported(declarator, f"shadowed/redeclared variable {name!r}")
        self.variable_types[name] = (
            (VAR_POINTER, (type_name,)) if is_array else (type_name,)
        )
        if parameter and is_array:
            self.array_parameters.add(name)
        declaration_type = Parameter if parameter else Declaration
        statements = [declaration_type(name)]
        if initializer is None:
            return statements
        if not is_array:
            statements.append(Assignment(name, self.read_pure_expression(initializer)))
        elif (
            declarator.type == "array_declarator"
            and initializer.type == "initializer_list"
        ):
            statements.extend(self._array_initialization(name, declarator, initializer))
        else:
            self._unsupported(initializer, "pointer aliases and aggregate initializers")
        return statements

    def _array_initialization(self, name: str, declarator: Node, initializer: Node):
        values = [
            child for child in initializer.named_children if child.type != "comment"
        ]
        size_node = declarator.child_by_field_name("size")
        if size_node is None:
            size = len(values)
        else:
            try:
                size = int(source_text(size_node), 0)
            except ValueError:
                self._unsupported(size_node, "array initializer needs a constant size")
        if len(values) > size:
            raise ValueError(f"Too many initializer values for {name}")
        assignments = []
        for index in range(size):
            value = (
                self.read_pure_expression(values[index]) if index < len(values) else "0"
            )
            assignments.append(ArrayAssignment(name, str(index), value))
        return assignments

    def make_assignment(self, left: Node, right: str):
        if left.type == "identifier":
            target = source_text(left)
            if self.variable_types[target][0] == VAR_POINTER:
                self._unsupported(
                    left, "pointer reassignment and whole-array assignment"
                )
            return Assignment(target, right)
        if left.type == "subscript_expression":
            array = left.child_by_field_name("argument")
            if array.type != "identifier":
                self._unsupported(left, "only one-dimensional array access")
            index = self.read_pure_expression(left.child_by_field_name("index"))
            return ArrayAssignment(source_text(array), index, right)
        self._unsupported(left, "assignment target")

    def parse_expression_updates(self, node: Node) -> list[Statement]:
        if node.type == "expression_statement":
            return (
                self.parse_expression_updates(node.named_children[0])
                if node.named_children
                else []
            )
        if node.type == "parenthesized_expression":
            return self.parse_expression_updates(node.named_children[0])
        if node.type == "comma_expression":
            return self.parse_expression_updates(
                node.child_by_field_name("left")
            ) + self.parse_expression_updates(node.child_by_field_name("right"))
        if node.type == "assignment_expression":
            left = node.child_by_field_name("left")
            right = self.read_pure_expression(node.child_by_field_name("right"))
            operator = source_text(node.child_by_field_name("operator"))
            if operator != "=":
                if operator not in ("+=", "-=", "*=", "/=", "%="):
                    self._unsupported(node, f"operator {operator}")
                right = f"({self.read_pure_expression(left)}) {operator[:-1]} ({right})"
            return [self.make_assignment(left, right)]
        if node.type == "update_expression":
            left = node.child_by_field_name("argument")
            operator = source_text(node.child_by_field_name("operator"))
            sign = "+" if operator == "++" else "-"
            return [
                self.make_assignment(
                    left, f"({self.read_pure_expression(left)}) {sign} 1"
                )
            ]
        self._unsupported(node, "expression statement")

    def parse_conditional(self, node: Node, depth: int, terminal=False):
        condition = self.read_pure_expression(node.child_by_field_name("condition"))
        then_body = self.parse_statement(
            node.child_by_field_name("consequence"), depth + 1, terminal
        )
        alternative = node.child_by_field_name("alternative")
        else_body = (
            self.parse_statement(alternative.named_children[0], depth + 1, terminal)
            if alternative is not None
            else []
        )
        return Conditional([(condition, then_body), (f"!({condition})", else_body)])

    def parse_loop(self, node: Node, depth: int):
        condition = node.child_by_field_name("condition")
        guard = (
            self.read_pure_expression(condition) if condition is not None else "true"
        )
        body = self.parse_statement(node.child_by_field_name("body"), depth + 1)
        update = node.child_by_field_name("update")
        if update is not None:
            body.extend(self.parse_expression_updates(update))
        # Postorder keeps inner loops available when verifying their enclosing loop.
        loop_id = len(self.loop_syntax_nodes)
        self.loop_syntax_nodes.append(node)
        dependencies = variable_dependencies(body)
        for values in dependencies.values():
            values.update(identifiers_in_expression(guard))
        return Loop(guard, body, depth, loop_id, None, dependencies)

    def _attach_postcondition(self, statements, annotation, source):
        for loop_index in range(len(statements) - 1, -1, -1):
            if isinstance(statements[loop_index], Loop):
                break
        else:
            self._unsupported(source, "assertion must follow a loop in the same block")
        loop = statements[loop_index]
        post_statements = statements[loop_index + 1 :]
        if loop.postcondition is not None:
            if post_statements != loop.post_statements:
                self._unsupported(source, "multiple assertions separated by statements")
            loop.postcondition = f"({loop.postcondition}) && ({annotation.expression})"
        else:
            loop.post_statements = post_statements
            loop.postcondition = annotation.expression

    def parse_block(self, node: Node, depth: int, terminal=False):
        statements = []
        children = node.named_children
        for index, child in enumerate(children):
            if child.type == "comment":
                annotation = parse_annotation(child)
                if isinstance(annotation, Assertion):
                    self._attach_postcondition(statements, annotation, child)
                elif annotation is not None:
                    statements.append(annotation)
            elif child.type == "return_statement":
                # A final, pure return does not affect any preceding loop obligation.
                remaining = children[index + 1 :]
                if not terminal or any(item.type != "comment" for item in remaining):
                    self._unsupported(child, "early return")
                for value in child.named_children:
                    self.read_pure_expression(value)
                if any(parse_annotation(item) is not None for item in remaining):
                    self._unsupported(child, "verification annotation after return")
                break
            else:
                is_terminal = terminal and all(
                    item.type == "comment" for item in children[index + 1 :]
                )
                statements.extend(self.parse_statement(child, depth, is_terminal))
        return statements

    def parse_statement(
        self, node: Node, depth: int, terminal=False
    ) -> list[Statement]:
        """A terminal statement has no executable successor on its function path."""
        if node.type == "compound_statement":
            return self.parse_block(node, depth, terminal)
        if node.type == "declaration":
            return self.parse_declaration(node)
        if node.type == "expression_statement":
            return self.parse_expression_updates(node)
        if node.type == "if_statement":
            return [self.parse_conditional(node, depth, terminal)]
        if node.type == "return_statement" and terminal:
            for value in node.named_children:
                self.read_pure_expression(value)
            return []
        if node.type in ("while_statement", "for_statement"):
            result = []
            initializer = node.child_by_field_name("initializer")
            if initializer is not None:
                result.extend(
                    self.parse_declaration(initializer)
                    if initializer.type == "declaration"
                    else self.parse_expression_updates(initializer)
                )
            result.append(self.parse_loop(node, depth))
            return result
        self._unsupported(node)

    def parse_function(
        self, function: Node
    ) -> tuple[dict[str, CType], list[Statement], str]:
        declarator = function.child_by_field_name("declarator")
        if declarator.type != "function_declarator":
            self._unsupported(declarator, "function return declarator")
        parameters = declarator.child_by_field_name("parameters")
        body = []
        for parameter in parameters.named_children:
            if parameter.type != "comment":
                body.extend(self.parse_declaration(parameter, parameter=True))
        if len(self.array_parameters) > 1:
            self._unsupported(parameters, "multiple pointer/array parameters may alias")
        body.extend(
            self.parse_block(function.child_by_field_name("body"), 0, terminal=True)
        )
        return (
            self.variable_types,
            body,
            source_text(function.child_by_field_name("type")),
        )


def parse_function(state: WorkflowState) -> WorkflowState:
    parser = FunctionParser()
    function = state["function"]
    types, body, return_type = parser.parse_function(function["syntax_node"])
    function.update(
        variable_types=types,
        statements=body,
        return_type=return_type,
        loop_syntax_nodes=parser.loop_syntax_nodes,
    )
    return {"function": function}
