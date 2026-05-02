<<<<<<< HEAD
# Mojeshlang

Mojeshlang is a lightweight, strictly evaluated, dynamically typed interpreted programming language implemented entirely in Python. Designed with a focus on pedagogical clarity and extensibility, Mojeshlang serves as a robust exploration of compiler theory and programming language design.

## Architecture & Design Patterns

The implementation of Mojeshlang heavily relies on classical design patterns to ensure a clean separation of concerns and maintainable architecture:

- **Interpreter Pattern**: At the core of Mojeshlang is the Interpreter pattern. The AST (Abstract Syntax Tree) nodes (e.g., `Program`, `BinaryExpression`, `IfStatement`) each represent grammatical rules. The `Interpreter` evaluates these nodes recursively, elegantly mapping the language's grammar to executable Python logic.
- **Lexical Analysis (Lexer)**: A custom tokenizer that linearly scans source code, transforming raw character streams into discrete semantic tokens using a lookahead mechanism.
- **Recursive Descent Parsing**: The `Parser` employs a top-down, recursive descent strategy to construct the AST, inherently enforcing operator precedence and grammatical correctness through deep call stacks.
- **Virtual Machine & Bytecode Compilation**: To explore lower-level execution models, Mojeshlang includes a bytecode compiler (`compiler.py`) and a stack-based virtual machine (`vm.py`), demonstrating an understanding of intermediate representation (IR) execution.

## Key Contributions

- **Standard Library Native Hooks ("Antigravity")**: Designed a bridging mechanism to execute high-level Python libraries (such as `urllib` and `json`) directly from Mojeshlang. This demonstrates how standard libraries can be intercepted and executed via native wrappers without dragging down AST evaluation.
- **Robust Scoping Mechanism**: Implemented dynamic variable scoping and function environments, ensuring isolated execution contexts and preventing scope leakage during deep recursive calls.
- **Comprehensive AST Construction**: Built a full suite of AST nodes supporting arithmetic operations, boolean logic, control flow (`if/while`), and user-defined functions.

## Project Structure

```text
Mojeshlang/
├── src/
│   ├── lexer.py         # Transforms raw source code into Tokens
│   ├── tokens.py        # Token classifications and Enums
│   ├── parser.py        # Recursive descent parser generating the AST
│   ├── ast_nodes.py     # Definitions for all Abstract Syntax Tree nodes
│   ├── interpreter.py   # Tree-walking interpreter for direct AST execution
│   ├── compiler.py      # Translates AST into linear bytecode instructions
│   ├── vm.py            # Stack-based Virtual Machine for bytecode execution
│   └── main.py          # Script entry point and execution loop
├── examples/            # Example Mojeshlang scripts
└── README.md            # Project documentation
```

## Performance Goals

As Mojeshlang scales, the following performance and memory optimization goals are actively targeted:

1. **Lazy Lexical Evaluation**: Transitioning the lexer to a generator-based model (`yield`) to stream tokens on-demand, significantly reducing `O(N)` memory overhead for massive source files.
2. **String Interning**: Utilizing Python's `sys.intern()` to memoize identifier allocations, preventing redundant memory allocations for recurring variables and keywords.
3. **Optimized Lookahead Buffering**: Moving from array-backed token streams to a sliding-window lookahead buffer within the parser, achieving `O(1)` memory complexity during the parsing phase.
4. **Bytecode Execution Optimization**: Gradually shifting primary execution pipelines from the tree-walking interpreter to the highly optimized stack-based Virtual Machine.

## How to Contribute

Contributions are welcome from developers interested in language design, memory optimization, and compiler architecture.

1. **Fork the Repository**: Create your feature branch (`git checkout -b feature/AmazingOptimization`).
2. **Understand the Pipeline**: Familiarize yourself with the `Lexer -> Parser -> AST -> Interpreter` pipeline before modifying nodes.
3. **Commit your Changes**: Ensure your commit messages clearly describe the architectural or algorithmic impact of your changes.
4. **Push to the Branch**: `git push origin feature/AmazingOptimization`.
5. **Open a Pull Request**: Detail the problem solved, the design pattern utilized, and any Big-O complexity improvements.

---
*Developed to rigorously explore the depths of Computer Science fundamentals.*
=======
# 🚀 Mojeshlang

A custom-built programming language with its own compiler, bytecode virtual machine, and desktop IDE.

---

## ✨ Features

- 🧠 Custom Lexer & Parser
- 🌳 Abstract Syntax Tree (AST)
- ⚙️ Bytecode Compiler
- 🔥 Stack-based Virtual Machine
- 🔁 Control Flow (if / else, while)
- 📞 Function Support (call stack + return values)
- 🖥️ Tkinter-based IDE
- 🎨 Syntax Highlighting
- 🧾 Bytecode Viewer

## 📌 Example

```mj
func add(a, b) {
    return a + b
}

print(add(10, 20))
>>>>>>> da183d4a413fd69dae6bb7d24a6878ae334c0704
