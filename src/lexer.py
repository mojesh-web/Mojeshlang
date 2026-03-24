from tokens import Token, TokenType


class Lexer:
    KEYWORDS = {
        "let": TokenType.LET,
        "print": TokenType.PRINT,
        "if": TokenType.IF,
        "while": TokenType.WHILE,
        "func": TokenType.FUNC,
        "else": TokenType.ELSE,
        "return": TokenType.RETURN,
    }

    def __init__(self, source_code):
        self.source = source_code
        self.position = 0
        self.tokens = []

    def peek(self):
        if self.position >= len(self.source):
            return None
        return self.source[self.position]

    def advance(self):
        char = self.peek()
        self.position += 1
        return char

    def match(self, expected):
        if self.peek() == expected:
            self.position += 1
            return True
        return False

    def skip_whitespace(self):
        while self.peek() is not None and self.peek().isspace():
            self.advance()

    def read_number(self):
        number = ""
        while self.peek() is not None and self.peek().isdigit():
            number += self.advance()
        return Token(TokenType.NUMBER, int(number))

    def read_identifier(self):
        identifier = ""
        while self.peek() is not None and (self.peek().isalnum() or self.peek() == "_"):
            identifier += self.advance()

        token_type = self.KEYWORDS.get(identifier, TokenType.IDENTIFIER)
        return Token(token_type, identifier)

    def tokenize(self):
        while self.peek() is not None:
            self.skip_whitespace()
            current = self.peek()

            if current is None:
                break

            if current.isdigit():
                self.tokens.append(self.read_number())

            elif current.isalpha() or current == "_":
                self.tokens.append(self.read_identifier())

            elif current == "=":
                self.advance()
                if self.match("="):
                    self.tokens.append(Token(TokenType.EQUAL_EQUAL, "=="))
                else:
                    self.tokens.append(Token(TokenType.EQUAL, "="))

            elif current == "!":
                self.advance()
                if self.match("="):
                    self.tokens.append(Token(TokenType.BANG_EQUAL, "!="))
                else:
                    raise SyntaxError("Unexpected character: !")

            elif current == ">":
                self.advance()
                if self.match("="):
                    self.tokens.append(Token(TokenType.GREATER_EQUAL, ">="))
                else:
                    self.tokens.append(Token(TokenType.GREATER, ">"))

            elif current == "<":
                self.advance()
                if self.match("="):
                    self.tokens.append(Token(TokenType.LESS_EQUAL, "<="))
                else:
                    self.tokens.append(Token(TokenType.LESS, "<"))

            elif current == "+":
                self.advance()
                self.tokens.append(Token(TokenType.PLUS, "+"))

            elif current == "-":
                self.advance()
                self.tokens.append(Token(TokenType.MINUS, "-"))

            elif current == "*":
                self.advance()
                self.tokens.append(Token(TokenType.STAR, "*"))

            elif current == "/":
                self.advance()
                self.tokens.append(Token(TokenType.SLASH, "/"))

            elif current == "(":
                self.advance()
                self.tokens.append(Token(TokenType.LPAREN, "("))

            elif current == ")":
                self.advance()
                self.tokens.append(Token(TokenType.RPAREN, ")"))

            elif current == "{":
                self.advance()
                self.tokens.append(Token(TokenType.LBRACE, "{"))

            elif current == "}":
                self.advance()
                self.tokens.append(Token(TokenType.RBRACE, "}"))

            elif current == ",":
                self.advance()
                self.tokens.append(Token(TokenType.COMMA, ","))

            else:
                raise SyntaxError(f"Unexpected character: {current}")

        self.tokens.append(Token(TokenType.EOF, None))
        return self.tokens