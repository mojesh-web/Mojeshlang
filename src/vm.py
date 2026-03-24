from bytecode import OpCode


class Frame:
    def __init__(self, return_ip, variables):
        self.return_ip = return_ip
        self.variables = variables


class VirtualMachine:
    def __init__(self):
        self.stack = []
        self.variables = {}
        self.functions = {}
        self.call_stack = []

    def run(self, instructions, functions):
        self.functions = functions
        ip = 0

        while ip < len(instructions):
            opcode, arg = instructions[ip]

            # BASIC
            if opcode == OpCode.LOAD_CONST:
                self.stack.append(arg)

            elif opcode == OpCode.LOAD_NAME:
                self.stack.append(self.variables.get(arg, 0))

            elif opcode == OpCode.STORE_NAME:
                self.variables[arg] = self.stack.pop()

            # MATH
            elif opcode == OpCode.ADD:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a + b)

            elif opcode == OpCode.SUB:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a - b)

            elif opcode == OpCode.MUL:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a * b)

            elif opcode == OpCode.DIV:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a / b)

            # COMPARE
            elif opcode == OpCode.COMPARE:
                b = self.stack.pop()
                a = self.stack.pop()

                if arg == ">":
                    self.stack.append(a > b)
                elif arg == "<":
                    self.stack.append(a < b)
                elif arg == ">=":
                    self.stack.append(a >= b)
                elif arg == "<=":
                    self.stack.append(a <= b)
                elif arg == "==":
                    self.stack.append(a == b)
                elif arg == "!=":
                    self.stack.append(a != b)

            # CONTROL FLOW
            elif opcode == OpCode.JUMP_IF_FALSE:
                if not self.stack.pop():
                    ip = arg
                    continue

            elif opcode == OpCode.JUMP:
                ip = arg
                continue

            # PRINT
            elif opcode == OpCode.PRINT:
                print(self.stack.pop())

            # FUNCTION CALL (REAL IMPLEMENTATION)
            elif opcode == OpCode.CALL:
                name, argc = arg

                if name not in self.functions:
                    raise Exception(f"Function '{name}' not defined")

                func_start, params = self.functions[name]

                # Save current state
                frame = Frame(ip + 1, self.variables.copy())
                self.call_stack.append(frame)

                # Create new local scope
                new_vars = {}

                # Assign arguments (correct order)
                for i in reversed(range(argc)):
                    new_vars[params[i]] = self.stack.pop()

                self.variables = new_vars

                # Jump to function
                ip = func_start
                continue

            # RETURN
            elif opcode == OpCode.RETURN:
                return_value = self.stack.pop()

                if not self.call_stack:
                    return

                frame = self.call_stack.pop()

                self.variables = frame.variables
                ip = frame.return_ip

                self.stack.append(return_value)
                continue

            ip += 1