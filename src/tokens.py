from enum import Enum, auto


class TokenType(Enum):
    # Keywords
    LET = auto()
    PRINT = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FUNC = auto()
    RETURN = auto()

    # Identifiers / literals
    IDENTIFIER = auto()
    NUMBER = auto()

    # Operators
    EQUAL = auto()          # =
    EQUAL_EQUAL = auto()    # ==
    BANG_EQUAL = auto()     # !=
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()

    # Punctuation
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    COMMA = auto()

    EOF = auto()


class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"