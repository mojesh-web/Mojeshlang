import sys
import time
import webbrowser
from lexer import Lexer
from parser import Parser
from compiler import Compiler
from vm import VirtualMachine

def antigravity_easter_egg():
    frames = [
        r"""
           ^
          / \
         /   \
        |     |
        |     |
        |     |
        |_____|
       /       \
      /         \
        """,
        r"""
           ^
          / \
         /   \
        |     |
        |     |
        |     |
        |_____|
       /       \
      /         \
         / \
        """,
        r"""
           ^
          / \
         /   \
        |     |
        |     |
        |     |
        |_____|
       /       \
      /         \
        ( * )
        """,
        r"""
           ^
          / \
         /   \
        |     |
        |     |
        |     |
        |_____|
       /       \
      /         \
       { *** }
        """
    ]
    
    # Animate rocket
    print("\nInitializing antigravity module...")
    time.sleep(1)
    
    for _ in range(3):
        for frame in frames:
            # Clear screen ANSI code
            print("\033[2J\033[H", end="")
            print(frame)
            time.sleep(0.15)
            
    print("Lift off! Opening GitHub repo...\n")
    time.sleep(1)
    # Replace this URL with your actual Mojeshlang repo
    webbrowser.open("https://github.com/mojesh-web/Mojeshlang")
def main():
    if len(sys.argv) < 2:
        print("Usage: python src/main.py <file.moj>")
        return

    try:
        with open(sys.argv[1], "r") as f:
            code = f.read()
    except FileNotFoundError:
        print(f"Error: Could not find file '{sys.argv[1]}'")
        return

    # 🔥 Intercept Easter Egg before Lexer to avoid syntax errors
    if "antigravity" in code:
        antigravity_easter_egg()
        # Remove the keyword so the parser doesn't crash on an unknown identifier!
        code = code.replace("antigravity", "")
        if not code.strip():
            return # Script was just the easter egg, nothing left to parse

    # 1. Lexical Analysis
    lexer = Lexer(code)
    tokens = lexer.tokenize()

    # 2. Syntax Parsing (AST)
    parser = Parser(tokens)
    ast = parser.parse()

    # 3. Compilation (AST -> Bytecode)
    compiler = Compiler()
    compiler.compile(ast)
    instructions, functions = compiler.get_instructions()

    # 4. Execution (Virtual Machine)
    vm = VirtualMachine()
    vm.run(instructions, functions)

if __name__ == "__main__":
    main()