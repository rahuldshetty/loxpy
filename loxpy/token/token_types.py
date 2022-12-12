from enum import Enum, auto

class TokenType(Enum):
    # Single-Character 
    LEFT_PARAN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    DIVIDE = auto()
    MULTIPLY = auto()
    SEMICOLON = auto()

    # One or Two character
    NOT = auto()
    NOT_EQUAL = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESSER = auto()
    LESSER_EQUAL = auto()

    # Literals
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    # Keywords
    AND = auto()
    OR = auto()

    CLASS = auto()
    
    NULL = auto()
    TRUE = auto()
    FALSE = auto()

    IF = auto()
    ELSE = auto()
    FUNCTION = auto()
    FOR = auto()

    PRINT = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto()
    VAR = auto()
    WHILE = auto()
    BREAK = auto()

    EOF = auto()


# Keyword Map
KEYWORD_MAP = {
    "and": TokenType.AND,
    "or": TokenType.OR,

    "class": TokenType.CLASS,

    "null": TokenType.NULL,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,

    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "fn": TokenType.FUNCTION,
    "for": TokenType.FOR,

    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "var": TokenType.VAR,
    "while": TokenType.WHILE,
    "break": TokenType.BREAK,
}
