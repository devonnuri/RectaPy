from enum import Enum, auto


class TokenType(Enum):
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    SEMICOLON = auto()

    COMMA = auto()
    DOT = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()

    EQUAL = auto()
    EQUAL_EQUAL = auto()
    EXCLAM = auto()
    EXCLAM_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()

    IDENTIFIER = auto()

    BOOLEAN = auto()
    NUMBER = auto()
    SINGLE_STRING = auto()
    DOUBLE_STRING = auto()

    IF = 'if'
    ELSE = 'else'
    AND = 'and'
    OR = 'or'
    TRUE = 'true'
    FALSE = 'false'
    FOR = 'for'
    WHILE = 'while'
    RETURN = 'return'

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)
