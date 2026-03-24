from bytecode import OpCode
from ast_nodes import *


class Compiler:
    def __init__(self):
        self.instructions = []
        self.functions = {}

    def compile(self, node):
        # ---------- PROGRAM ----------
        if isinstance(node, Program):
            for stmt in node.statements:
                self.compile(stmt)

        # ---------- VARIABLES ----------
        elif isinstance(node, LetStatement):
            self.compile(node.value)
            self.emit(OpCode.STORE_NAME, node.name)

        elif isinstance(node, AssignmentStatement):
            self.compile(node.value)
            self.emit(OpCode.STORE_NAME, node.name)

        # ---------- PRINT ----------
        elif isinstance(node, PrintStatement):
            self.compile(node.expression)
            self.emit(OpCode.PRINT)

        # ---------- LITERALS ----------
        elif isinstance(node, NumberLiteral):
            self.emit(OpCode.LOAD_CONST, node.value)

        elif isinstance(node, Identifier):
            self.emit(OpCode.LOAD_NAME, node.name)

        # ---------- EXPRESSIONS ----------
        elif isinstance(node, BinaryExpression):
            self.compile(node.left)
            self.compile(node.right)

            if node.operator == "+":
                self.emit(OpCode.ADD)
            elif node.operator == "-":
                self.emit(OpCode.SUB)
            elif node.operator == "*":
                self.emit(OpCode.MUL)
            elif node.operator == "/":
                self.emit(OpCode.DIV)
            else:
                self.emit(OpCode.COMPARE, node.operator)

        # ---------- IF ----------
        elif isinstance(node, IfStatement):
            self.compile(node.condition)

            jump_false = self.emit(OpCode.JUMP_IF_FALSE, None)

            # THEN
            for stmt in node.then_branch:
                self.compile(stmt)

            jump_end = self.emit(OpCode.JUMP, None)

            # ELSE
            self.patch(jump_false)

            if node.else_branch:
                for stmt in node.else_branch:
                    self.compile(stmt)

            self.patch(jump_end)

        # ---------- WHILE ----------
        elif isinstance(node, WhileStatement):
            loop_start = len(self.instructions)

            self.compile(node.condition)

            jump_false = self.emit(OpCode.JUMP_IF_FALSE, None)

            for stmt in node.body:
                self.compile(stmt)

            self.emit(OpCode.JUMP, loop_start)

            self.patch(jump_false)

        # ---------- FUNCTION ----------
        elif isinstance(node, FunctionDeclaration):
            # 🔥 Skip function during main execution
            jump_over = self.emit(OpCode.JUMP, None)

            func_start = len(self.instructions)

            # Store function location + params
            self.functions[node.name] = (func_start, node.params)

            # Compile function body
            for stmt in node.body:
                self.compile(stmt)

            # Default return if not provided
            self.emit(OpCode.LOAD_CONST, None)
            self.emit(OpCode.RETURN)

            # Patch jump to skip function body
            self.patch(jump_over)

        # ---------- FUNCTION CALL ----------
        elif isinstance(node, CallExpression):
            for arg in node.arguments:
                self.compile(arg)

            self.emit(OpCode.CALL, (node.callee, len(node.arguments)))

        # ---------- RETURN ----------
        elif isinstance(node, ReturnStatement):
            self.compile(node.value)
            self.emit(OpCode.RETURN)

        # ---------- ERROR ----------
        else:
            raise Exception(f"Unsupported node: {type(node).__name__}")

    # ---------- EMIT ----------
    def emit(self, opcode, arg=None):
        self.instructions.append((opcode, arg))
        return len(self.instructions) - 1

    # ---------- PATCH JUMPS ----------
    def patch(self, index):
        opcode, _ = self.instructions[index]
        self.instructions[index] = (opcode, len(self.instructions))

    # ---------- OUTPUT ----------
    def get_instructions(self):
        return self.instructions, self.functions