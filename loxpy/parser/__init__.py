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
            # Class Declaration
            if self.match(TokenType.CLASS):
                return self.class_declaraction()

            # Function declaration
            if self.match(TokenType.FUNCTION):
                return self.function("function")

            # Var declaration
            if self.match(TokenType.VAR):
                return self.var_declaration()
            return self.statement()
        except ParserError as parse_error:
            self.synchronize()

    def statement(self):
        # For Statement
        if self.match(TokenType.FOR):
            return self.for_statement()

        # Break Statement
        if self.match(TokenType.BREAK):
            return self.break_statement()

        # If Statement
        if self.match(TokenType.IF):
            return self.if_statement()

        # Print Statement
        if self.match(TokenType.PRINT):
            return self.print_statement()

        # Return Statement
        if self.match(TokenType.RETURN):
            return self.return_statement()
        
        # While Statement
        if self.match(TokenType.WHILE):
            return self.while_statement()

        # Block Statement
        if self.match(TokenType.LEFT_BRACE):
            return statements.Block(self.block())
        
        return self.expression_statement()

    def if_statement(self):
        self.consume(TokenType.LEFT_PARAN, "Expected '(' after 'if'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expected ')' after condition.")

        thenBranch = self.statement()
        
        elseBranch = None
        if self.match(TokenType.ELSE):
            elseBranch = self.statement()
        
        return statements.If(condition, thenBranch, elseBranch)


    def for_statement(self):
        '''
        Desugaring, convert 'for' statement into 'while' to re-use existing statement.
        '''
        self.consume(TokenType.LEFT_PARAN, "Expected '(' after for statement.")
        
        # Initializer Expression
        initializer = None
        if self.match(TokenType.SEMICOLON):
            initializer = None
        elif self.match(TokenType.VAR):
            initializer = self.var_declaration()
        else:
            initializer = self.expression_statement()
        
        # Condition Expression
        condition = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after loop condition.")

        # Increment Expression
        increment = None
        if not self.check(TokenType.RIGHT_PAREN):
            increment = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expected ')' after increment clauses.")

        # For loop body
        body = self.statement()

        # Prepare While Statement with initializer, condition and increment
        if increment != None:
            body = statements.Block([
                body,
                statements.Expression(increment)
            ])

        if condition == None:
            condition = expressions.Literal(True)

        body = statements.While(condition, body)

        if initializer != None:
            body = statements.Block([
                initializer, body
            ])

        return body

    def function(self, kind:str):
        name = self.consume(TokenType.IDENTIFIER, "Expected " + kind + " name.")

        self.consume(TokenType.LEFT_PARAN, "Expected '(' after " + kind + " name.")
        
        params = []
        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                if len(params) >= 255:
                    self.error(self.peek(), "Can't have more than 255 parameters.")
                params.append(
                    self.consume(TokenType.IDENTIFIER, "Expected parameter name.")
                )

                if not self.match(TokenType.COMMA):
                    break
        self.consume(TokenType.RIGHT_PAREN, "Expected ')' after parameters.")

        self.consume(TokenType.LEFT_BRACE, "Expected '{' before " + kind + " body.")
        body = self.block()
        
        return statements.Function(name, params, body)

    def return_statement(self):
        keyword = self.previous()
        value = None
        if not self.check(TokenType.SEMICOLON):
            value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after return value.")
        return statements.Return(keyword, value)

    def break_statement(self):
        self.consume(TokenType.SEMICOLON, "Expected ';' after break statement.")
        return statements.Break(self.previous())

    def block(self):
        statements = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            statements.append(self.declaration())
        
        self.consume(TokenType.RIGHT_BRACE, "Expected '}' after block.")
        return statements

    def class_declaraction(self):
        name = self.consume(TokenType.IDENTIFIER, "Expected class name.")
        self.consume(TokenType.LEFT_BRACE, "Expected '{' before class body.")

        methods = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            self.consume(TokenType.FUNCTION, "Expected method declaraction.")
            methods.append(self.function("method"))
        
        self.consume(TokenType.RIGHT_BRACE, "Expected '}' after class body.")
        
        return statements.Class(name, methods)


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
        expr = self.logical_or()

        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()

            if type(expr) == expressions.Variable:
                # Variable assignment
                name = expr.name
                return expressions.Assign(name, value)
            elif isinstance(expr, expressions.Dot):
                # Class instance dot set operator
                return expressions.DotSet(expr.object, expr.name, value)
            
            raise self.error(equals, "Invalid assignment target.")

        return expr

    def while_statement(self):
        self.consume(TokenType.LEFT_PARAN, "Expected '(' after while statement.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expected ')' after condition expression.")
        body = self.statement()
        return statements.While(condition, body)

    def logical_or(self):
        expr = self.logical_and()
        while self.match(TokenType.OR):
            operator = self.previous()
            right = self.logical_and()
            expr = expressions.Logical(expr, operator, right)
        return expr

    def logical_and(self):
        expr = self.equality()
        while self.match(TokenType.AND):
            operator = self.previous()
            right = self.equality()
            expr = expressions.Logical(expr, operator, right)
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
        return self.call()

    def call(self):
        expr = self.primary()
        while True:
            if self.match(TokenType.LEFT_PARAN):
                expr = self.finish_call(expr)
            elif self.match(TokenType.DOT):
                name = self.consume(TokenType.IDENTIFIER, "Expected property name after dot operator.")
                expr = expressions.Dot(expr, name)
            else:
                break
        return expr
    
    def finish_call(self, callee: expressions.Expr):
        arguments = []
        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                if len(arguments) >= 255:
                    self.lox.error(self.peek(), "Can't have more than 255 arguments.")
                arguments.append(
                    self.expression()
                )
                if not self.match(TokenType.COMMA):
                    break
        paren = self.consume(TokenType.RIGHT_PAREN, "Expected ')' after arguments.")
        return expressions.Call(callee, paren, arguments)
    
    def primary(self):
        if self.match(TokenType.FALSE):
            return expressions.Literal(False)
        if self.match(TokenType.TRUE):
            return expressions.Literal(True)
        if self.match(TokenType.NULL):
            return expressions.Literal(None)
        
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return expressions.Literal(self.previous().literal)
        
        if self.match(TokenType.THIS):
            return expressions.This(self.previous())

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
    



