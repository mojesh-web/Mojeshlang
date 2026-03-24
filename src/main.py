from lexer import Lexer
from parser import Parser
from compiler import Compiler
from vm import VirtualMachine
import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: python src/main.py <file>")
        return

    with open(sys.argv[1], "r") as f:
        code = f.read()

    lexer = Lexer(code)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse()

    compiler = Compiler()
    compiler.compile(ast)

    instructions, functions = compiler.get_instructions()

    vm = VirtualMachine()
    vm.run(instructions, functions)


if __name__ == "__main__":
    main()