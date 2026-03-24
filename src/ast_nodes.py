class Program:
    def __init__(self, statements):
        self.statements = statements


class LetStatement:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class AssignmentStatement:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class PrintStatement:
    def __init__(self, expression):
        self.expression = expression


class IfStatement:
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch


class WhileStatement:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


# 🔥 NEW (functions)
class FunctionDeclaration:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body


class CallExpression:
    def __init__(self, callee, arguments):
        self.callee = callee
        self.arguments = arguments


class ReturnStatement:
    def __init__(self, value):
        self.value = value


# Expressions
class NumberLiteral:
    def __init__(self, value):
        self.value = value


class Identifier:
    def __init__(self, name):
        self.name = name


class BinaryExpression:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right