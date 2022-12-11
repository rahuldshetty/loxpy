'''
Recursive Decent Parser for loxpy
'''
from loxpy.parser import expressions
from loxpy.token.token_types import TokenType

from loxpy.parser import statements

class ParserError(Exception):
    pass

class Parser:
    def __init__(self, tokens, lox_interpreter):
        self.current = 0
        self.tokens = tokens
        self.lox = lox_interpreter
    
    def parse(self):
        try:
            statements = []
            while not self.is_at_end():
                statements.append(self.declaration())

            return statements
        except ParserError as parse_error:
            return None

    def error(self, token, message):
        self.lox.error(token.line, message)
        return ParserError()

    def synchronize(self):
        self.advance()

        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return
            
            if self.peek().type in [
                TokenType.CLASS,
                TokenType.FUNCTION,
                TokenType.VAR,
                TokenType.FOR,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.PRINT,
                TokenType.RETURN
            ]:
                return
            
            self.advance()
    
    def declaration(self):
        try:
            if self.match(TokenType.VAR):
                return self.var_declaration()
            return self.statement()
        except ParserError as parse_error:
            self.synchronize()

    def statement(self):
        # Print Statement
        if self.match(TokenType.PRINT):
            return self.print_statement()
        
        return self.expression_statement()

    def var_declaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expected variable name.")

        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()

        self.consume(TokenType.SEMICOLON, "Expected ';' after variable declaraction.")
        return statements.Var(name, initializer)        

    def print_statement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after value.")
        return statements.Print(value)

    def expression_statement(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after expression.")
        return statements.Expression(expr)

    def expression(self):
        return self.assignment()
    
    def assignment(self):
        expr = self.equality()

        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()

            if type(expr) == expressions.Variable:
                name = expr.name
                return expressions.Assign(name, value)
            
            raise self.error(equals, "Invalid assignment target.")

        return expr

    def equality(self):
        expr = self.comparison()

        while self.match(TokenType.NOT_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = expressions.Binary(expr, operator, right)
        
        return expr

    def comparison(self):
        expr = self.term()

        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESSER, TokenType.LESSER_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = expressions.Binary(expr, operator, right)
        
        return expr

    def term(self):
        expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = expressions.Binary(expr, operator, right)
        
        return expr
    
    def factor(self):
        expr = self.unary()

        while self.match(TokenType.DIVIDE, TokenType.MULTIPLY):
            operator = self.previous()
            right = self.unary()
            expr = expressions.Binary(expr, operator, right)
        
        return expr

    def unary(self):
        if self.match(TokenType.NOT, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return expressions.Unary(operator, right)
        return self.primary()
    
    def primary(self):
        if self.match(TokenType.FALSE):
            return expressions.Literal(False)
        if self.match(TokenType.TRUE):
            return expressions.Literal(True)
        if self.match(TokenType.NULL):
            return expressions.Literal(None)
        
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return expressions.Literal(self.previous().literal)

        if self.match(TokenType.IDENTIFIER):
            return expressions.Variable(self.previous())

        if self.match(TokenType.LEFT_PARAN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expected ')' after expression.")
            return expressions.Grouping(expr)
        
        raise self.error(self.peek(), f"Invalid expression found.")
    
    def consume(self, token_type, message):
        if self.check(token_type):
            return self.advance()
        
        raise self.error(self.peek(), message)

    def match(self, *types):
        for typ in types:
            if self.check(typ):
                self.advance()
                return True
        return False

    def check(self, token_type):
        if self.is_at_end():
            return False
        return self.peek().type == token_type
    
    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()
    
    def is_at_end(self):
        return self.peek().type == TokenType.EOF
    
    def peek(self):
        return self.tokens[self.current]
    
    def previous(self):
        return self.tokens[self.current - 1]
    



