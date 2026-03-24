import tkinter as tk
from tkinter import filedialog, messagebox

from lexer import Lexer
from parser import Parser
from compiler import Compiler
from vm import VirtualMachine


class MojeshIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Mojeshlang IDE")
        self.root.geometry("900x650")

        # --------------------------
        # CODE EDITOR
        # --------------------------
        self.code_editor = tk.Text(
            root,
            height=20,
            width=80,
            bg="#1e1e1e",
            fg="white",
            insertbackground="white"
        )
        self.code_editor.pack(padx=10, pady=10)

        # Syntax highlighting colors
        self.code_editor.tag_config("keyword", foreground="#569CD6")
        self.code_editor.tag_config("number", foreground="#B5CEA8")
        self.code_editor.tag_config("identifier", foreground="#9CDCFE")

        self.code_editor.bind("<KeyRelease>", self.highlight_syntax)

        # --------------------------
        # BUTTONS
        # --------------------------
        button_frame = tk.Frame(root)
        button_frame.pack()

        tk.Button(button_frame, text="Run ▶", command=self.run_code).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Show Bytecode ⚙️", command=self.show_bytecode).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Open 📂", command=self.open_file).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Save 💾", command=self.save_file).pack(side=tk.LEFT, padx=5)

        # --------------------------
        # OUTPUT CONSOLE
        # --------------------------
        tk.Label(root, text="Output:").pack()
        self.output_console = tk.Text(root, height=8, bg="black", fg="white")
        self.output_console.pack(fill=tk.BOTH, padx=10, pady=5)

        # --------------------------
        # BYTECODE VIEW
        # --------------------------
        tk.Label(root, text="Bytecode:").pack()
        self.bytecode_view = tk.Text(root, height=8, bg="#222", fg="#00ff00")
        self.bytecode_view.pack(fill=tk.BOTH, padx=10, pady=5)

    # --------------------------
    # SYNTAX HIGHLIGHTING
    # --------------------------
    def highlight_syntax(self, event=None):
        code = self.code_editor.get("1.0", tk.END)

        # Remove old tags
        for tag in ["keyword", "number", "identifier"]:
            self.code_editor.tag_remove(tag, "1.0", tk.END)

        keywords = ["let", "print", "if", "else", "while", "func", "return"]

        words = code.split()
        index = "1.0"

        for word in words:
            start = self.code_editor.search(word, index, stopindex=tk.END)

            if not start:
                continue

            end = f"{start}+{len(word)}c"

            if word in keywords:
                self.code_editor.tag_add("keyword", start, end)
            elif word.isdigit():
                self.code_editor.tag_add("number", start, end)
            elif word.isidentifier():
                self.code_editor.tag_add("identifier", start, end)

            index = end

    # --------------------------
    # RUN CODE
    # --------------------------
    def run_code(self):
        code = self.code_editor.get("1.0", tk.END)

        self.output_console.delete("1.0", tk.END)

        try:
            lexer = Lexer(code)
            tokens = lexer.tokenize()

            parser = Parser(tokens)
            ast = parser.parse()

            compiler = Compiler()
            compiler.compile(ast)

            instructions, functions = compiler.get_instructions()

            vm = VirtualMachine()

            # Capture output
            import sys
            from io import StringIO

            old_stdout = sys.stdout
            sys.stdout = StringIO()

            vm.run(instructions, functions)

            output = sys.stdout.getvalue()
            sys.stdout = old_stdout

            self.output_console.insert(tk.END, output)

        except Exception as e:
            self.output_console.insert(tk.END, f"Error:\n{str(e)}")

    # --------------------------
    # SHOW BYTECODE
    # --------------------------
    def show_bytecode(self):
        code = self.code_editor.get("1.0", tk.END)

        self.bytecode_view.delete("1.0", tk.END)

        try:
            lexer = Lexer(code)
            tokens = lexer.tokenize()

            parser = Parser(tokens)
            ast = parser.parse()

            compiler = Compiler()
            compiler.compile(ast)

            instructions, _ = compiler.get_instructions()

            for instr in instructions:
                self.bytecode_view.insert(tk.END, str(instr) + "\n")

        except Exception as e:
            self.bytecode_view.insert(tk.END, f"Error:\n{str(e)}")

    # --------------------------
    # OPEN FILE
    # --------------------------
    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Mojesh Files", "*.mj")])
        if not file_path:
            return

        with open(file_path, "r") as f:
            code = f.read()

        self.code_editor.delete("1.0", tk.END)
        self.code_editor.insert(tk.END, code)

    # --------------------------
    # SAVE FILE
    # --------------------------
    def save_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".mj",
            filetypes=[("Mojesh Files", "*.mj")]
        )
        if not file_path:
            return

        code = self.code_editor.get("1.0", tk.END)

        with open(file_path, "w") as f:
            f.write(code)

        messagebox.showinfo("Saved", "File saved successfully!")


# --------------------------
# START IDE
# --------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = MojeshIDE(root)
    root.mainloop()