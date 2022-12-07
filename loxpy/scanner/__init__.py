from loxpy.token.token_types import TokenType
from loxpy.token import Token

class Scanner:
    def __init__(self, source, lox_interpreter):
        self.lox = lox_interpreter
        self.source = source
        self.tokens = []
        
        self.start = 0
        self.current = 0
        self.line = 1

    def scan_tokens(self):
        while not self.is_at_end():
            # current is at beginning of next token
            self.start = self.current
            self.scan_token()
        
        # Add EOF token 
        self.tokens.append(
            Token(
                TokenType.EOF,
                "",
                None,
                self.line
            )
        )
        return self.tokens

    
    def is_at_end(self):
        return self.current >= len(self.source)
    
    def is_digit(self, c):
        return c >= '0' and c <= '9'

    def scan_token(self):
        c = self.advance()

        # Single character token
        if c == "(":
            self.add_token(TokenType.LEFT_PARAN)
        elif c == ")":
            self.add_token(TokenType.RIGHT_PAREN)
        elif c == "{":
            self.add_token(TokenType.LEFT_BRACE)
        elif c == "}":
            self.add_token(TokenType.RIGHT_BRACE)
        elif c == ",":
            self.add_token(TokenType.COMMA)
        elif c == ".":
            self.add_token(TokenType.DOT) 
        elif c == "-":
            self.add_token(TokenType.MINUS)
        elif c == "+":
            self.add_token(TokenType.PLUS)
        elif c == ";":
            self.add_token(TokenType.SEMICOLON)
        elif c == "*":
            self.add_token(TokenType.MULTIPLY)

        # Double character token
        elif c == "!":
            self.add_token(
               TokenType.NOT_EQUAL if self.match('=') else TokenType.NOT
            )
        elif c == "=":
            self.add_token(
               TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL
            )
        elif c == "<":
            self.add_token(
               TokenType.LESSER_EQUAL if self.match('=') else TokenType.LESSER
            )
        elif c == ">":
            self.add_token(
               TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER
            )

        elif c == "/":
            if self.match("/"):
                # Keep advancing until new line for comment character found
                while self.peek() != '\n' and not self.is_at_end():
                    self.advance()
            else:
                self.add_token(TokenType.DIVIDE)

        # Skip over whitespace characters
        elif c in [' ', '\r', '\t']:
            return
        elif c == '\n':
            self.line += 1
            return

        # Parse "String" literal texts
        elif c == '"':
            self.match_string()

        else:
            # Parse number literals if
            if self.is_digit(c):
                self.match_number()

            # Unexpected character presented to lexer
            else:
                self.lox.error(self.line, "Unexpected character '" + c + "' found.")

    def advance(self):
        current_char = self.source[self.current]
        self.current += 1
        return current_char

    def peek(self):
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def match(self, expected):
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def match_string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line+=1
            self.advance()
        
        if self.is_at_end():
            self.lox.error(self.line, "Unterminated end of string.")
            return
        
        # the last "
        self.advance()

        value = self.source[self.start + 1: self.current - 1]
        self.add_token(TokenType.STRING, value)

    def match_number(self):
        while self.is_digit(self.peek()):
            self.advance()

        # Support fractional part
        if self.peek() == "." and self.is_digit(self.peek_next()):
            self.advance()

            while self.is_digit(self.peek()):
                self.advance()

        self.add_token(TokenType.NUMBER, float(self.source[self.start:self.current]))

    def add_token(self, token_type, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(
            token_type,
            text,
            literal,
            self.line
        ))