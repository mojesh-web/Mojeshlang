from lexer import Lexer
from parser import Parser
from compiler import Compiler
from vm import VirtualMachine
import sys
import time
import webbrowser

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
    webbrowser.open("https://github.com/your-username/Mojeshlang")

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/main.py <file>")
        return

    with open(sys.argv[1], "r") as f:
        code = f.read()

    # 🔥 Intercept Easter Egg before Lexer to avoid syntax errors
    if "antigravity" in code:
        antigravity_easter_egg()
        # Remove the keyword so the parser doesn't crash on an unknown identifier!
        code = code.replace("antigravity", "")
        if not code.strip():
            return # Script was just the easter egg, nothing left to parse

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