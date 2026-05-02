from tokens import TokenType
from ast_nodes import (
    Program,
    LetStatement,
    AssignmentStatement,
    PrintStatement,
    IfStatement,
    WhileStatement,
    FunctionDeclaration,
    CallExpression,
    ReturnStatement,
    NumberLiteral,
    Identifier,
    BinaryExpression,
)
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current_token(self):
        return self.tokens[self.position]

    def peek_next_token(self):
        if self.position + 1 < len(self.tokens):
            return self.tokens[self.position + 1]
        return None

    def advance(self):
        token = self.current_token()
        self.position += 1
        return token

    def expect(self, token_type):
        token = self.current_token()
        if token.type != token_type:
            raise SyntaxError(f"Expected {token_type}, got {token.type}")
        self.position += 1
        return token

    def parse(self):
        statements = []
        while self.current_token().type != TokenType.EOF:
            statements.append(self.parse_statement())
        return Program(statements)

    def parse_statement(self):
        current = self.current_token()

        if current.type == TokenType.LET:
            return self.parse_let_statement()

        elif current.type == TokenType.PRINT:
            return self.parse_print_statement()

        elif current.type == TokenType.IF:
            return self.parse_if_statement()

        elif current.type == TokenType.WHILE:
            return self.parse_while_statement()

        elif current.type == TokenType.FUNC:
            return self.parse_function()

        elif current.type == TokenType.RETURN:
            return self.parse_return_statement()

        elif (
            current.type == TokenType.IDENTIFIER
            and self.peek_next_token() is not None
            and self.peek_next_token().type == TokenType.EQUAL
        ):
            return self.parse_assignment_statement()

        else:
            raise SyntaxError(f"Unexpected statement: {current.type}")

    def parse_let_statement(self):
        self.expect(TokenType.LET)
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.EQUAL)
        value = self.parse_expression()
        return LetStatement(name, value)

    def parse_assignment_statement(self):
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.EQUAL)
        value = self.parse_expression()
        return AssignmentStatement(name, value)

    def parse_print_statement(self):
        self.expect(TokenType.PRINT)
        self.expect(TokenType.LPAREN)
        expr = self.parse_expression()
        self.expect(TokenType.RPAREN)
        return PrintStatement(expr)

    def parse_if_statement(self):
        self.expect(TokenType.IF)
        condition = self.parse_expression()
        then_branch = self.parse_block()

        else_branch = None
        if self.current_token().type == TokenType.ELSE:
            self.advance()
            else_branch = self.parse_block()

        return IfStatement(condition, then_branch, else_branch)

    def parse_while_statement(self):
        self.expect(TokenType.WHILE)
        condition = self.parse_expression()
        body = self.parse_block()
        return WhileStatement(condition, body)

    def parse_function(self):
        self.expect(TokenType.FUNC)
        name = self.expect(TokenType.IDENTIFIER).value

        self.expect(TokenType.LPAREN)
        params = []

        if self.current_token().type != TokenType.RPAREN:
            params.append(self.expect(TokenType.IDENTIFIER).value)
            while self.current_token().type == TokenType.COMMA:
                self.advance()
                params.append(self.expect(TokenType.IDENTIFIER).value)

        self.expect(TokenType.RPAREN)

        body = self.parse_block()
        return FunctionDeclaration(name, params, body)

    def parse_return_statement(self):
        self.expect(TokenType.RETURN)
        value = self.parse_expression()
        return ReturnStatement(value)

    def parse_block(self):
        self.expect(TokenType.LBRACE)
        statements = []

        while self.current_token().type != TokenType.RBRACE:
            if self.current_token().type == TokenType.EOF:
                raise SyntaxError("Missing '}'")
            statements.append(self.parse_statement())

        self.expect(TokenType.RBRACE)
        return statements

    def parse_expression(self):
        return self.parse_equality()

    def parse_equality(self):
        expr = self.parse_comparison()

        while self.current_token().type in (TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL):
            op = self.advance().value
            right = self.parse_comparison()
            expr = BinaryExpression(expr, op, right)

        return expr

    def parse_comparison(self):
        expr = self.parse_term()

        while self.current_token().type in (
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            op = self.advance().value
            right = self.parse_term()
            expr = BinaryExpression(expr, op, right)

        return expr

    def parse_term(self):
        expr = self.parse_factor()

        while self.current_token().type in (TokenType.PLUS, TokenType.MINUS):
            op = self.advance().value
            right = self.parse_factor()
            expr = BinaryExpression(expr, op, right)

        return expr

    def parse_factor(self):
        expr = self.parse_primary()

        while self.current_token().type in (TokenType.STAR, TokenType.SLASH):
            op = self.advance().value
            right = self.parse_primary()
            expr = BinaryExpression(expr, op, right)

        return expr

    def parse_primary(self):
        token = self.current_token()

        if token.type == TokenType.NUMBER:
            self.advance()
            return NumberLiteral(token.value)

        if token.type == TokenType.IDENTIFIER:
            self.advance()

            # 🔥 FUNCTION CALL
            if self.current_token().type == TokenType.LPAREN:
                self.advance()
                args = []

                if self.current_token().type != TokenType.RPAREN:
                    args.append(self.parse_expression())
                    while self.current_token().type == TokenType.COMMA:
                        self.advance()
                        args.append(self.parse_expression())

                self.expect(TokenType.RPAREN)
                return CallExpression(token.value, args)

            return Identifier(token.value)

        if token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr

        raise SyntaxError(f"Unexpected token: {token.type}")