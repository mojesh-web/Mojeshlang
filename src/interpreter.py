from ast_nodes import (
    Program,
    LetStatement,
    AssignmentStatement,
    PrintStatement,
    IfStatement,
    WhileStatement,
    FunctionDeclaration,
    CallExpression,
    ReturnStatement,
    NumberLiteral,
    Identifier,
    BinaryExpression,
)


# 🔥 Used to handle return flow
class ReturnException(Exception):
    def __init__(self, value):
        self.value = value


class Interpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}

    def interpret(self, node):
        if isinstance(node, Program):
            for statement in node.statements:
                self.interpret(statement)

        elif isinstance(node, LetStatement):
            value = self.evaluate(node.value)
            self.variables[node.name] = value

        elif isinstance(node, AssignmentStatement):
            if node.name not in self.variables:
                raise NameError(f"Variable '{node.name}' is not defined")
            value = self.evaluate(node.value)
            self.variables[node.name] = value

        elif isinstance(node, PrintStatement):
            value = self.evaluate(node.expression)
            print(value)

        elif isinstance(node, IfStatement):
            if self.evaluate(node.condition):
                self.execute_block(node.then_branch)
            elif node.else_branch:
                self.execute_block(node.else_branch)

        elif isinstance(node, WhileStatement):
            while self.evaluate(node.condition):
                self.execute_block(node.body)

        elif isinstance(node, FunctionDeclaration):
            self.functions[node.name] = node

        elif isinstance(node, ReturnStatement):
            value = self.evaluate(node.value)
            raise ReturnException(value)

        else:
            raise RuntimeError(f"Unknown node type: {type(node).__name__}")

    def execute_block(self, statements):
        for statement in statements:
            self.interpret(statement)

    def evaluate(self, node):
        if isinstance(node, NumberLiteral):
            return node.value

        elif isinstance(node, Identifier):
            if node.name not in self.variables:
                raise NameError(f"Variable '{node.name}' is not defined")
            return self.variables[node.name]

        elif isinstance(node, BinaryExpression):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            op = node.operator

            if op == "+":
                return left + right
            elif op == "-":
                return left - right
            elif op == "*":
                return left * right
            elif op == "/":
                return left / right
            elif op == ">":
                return left > right
            elif op == "<":
                return left < right
            elif op == ">=":
                return left >= right
            elif op == "<=":
                return left <= right
            elif op == "==":
                return left == right
            elif op == "!=":
                return left != right
            else:
                raise RuntimeError(f"Unknown operator: {op}")

        elif isinstance(node, CallExpression):
            func = self.functions.get(node.callee)

            if not func:
                raise NameError(f"Function '{node.callee}' not defined")

            if len(node.arguments) != len(func.params):
                raise RuntimeError("Argument count mismatch")

            # 🔥 Create NEW SCOPE
            old_vars = self.variables
            self.variables = {}

            # Assign arguments to parameters
            for i in range(len(func.params)):
                self.variables[func.params[i]] = self.evaluate(node.arguments[i])

            try:
                self.execute_block(func.body)
                result = None
            except ReturnException as ret:
                result = ret.value

            # 🔥 Restore OLD SCOPE
            self.variables = old_vars

            return result

        else:
            raise RuntimeError(f"Unknown expression node: {type(node).__name__}")