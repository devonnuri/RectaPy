from typing import List, Optional

from .token import Token
from .tokentype import TokenType
from rectapy import RectaSyntaxError


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

    def lex(self) -> List[Token]:
        while not self.is_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, ''))

        return self.tokens

    def scan_token(self) -> None:
        ch = self.advance()

        if ch == '(':
            self.add_token(TokenType.LEFT_PAREN)
        elif ch == ')':
            self.add_token(TokenType.RIGHT_PAREN)
        elif ch == '{':
            self.add_token(TokenType.LEFT_BRACE)
        elif ch == '}':
            self.add_token(TokenType.RIGHT_BRACE)
        elif ch == '[':
            self.add_token(TokenType.LEFT_BRACKET)
        elif ch == ']':
            self.add_token(TokenType.RIGHT_BRACKET)
        elif ch == ',':
            self.add_token(TokenType.COMMA)
        elif ch == '.':
            self.add_token(TokenType.DOT)
        elif ch == '-':
            self.add_token(TokenType.MINUS)
        elif ch == '+':
            self.add_token(TokenType.PLUS)
        elif ch == ';':
            self.add_token(TokenType.SEMICOLON)
        elif ch == '*':
            self.add_token(TokenType.STAR)
        elif ch == '!':
            self.add_token(TokenType.EXCLAM_EQUAL if self.match('=') else TokenType.EXCLAM)
        elif ch == '=':
            self.add_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
        elif ch == '<':
            self.add_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
        elif ch == '>':
            self.add_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
        elif ch == '/':
            if self.match('/'):
                while self.peek() != '\n' and not self.is_end():
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)
        elif ch.isspace():
            pass
        elif ch == '\n':
            self.line += 1
        elif ch == '"' or ch == '\'':
            while self.peek() != ch and not self.is_end():
                if self.peek() == '\n':
                    self.line += 1
                self.advance()

            if self.is_end():
                raise RectaSyntaxError('Unterminated string')

            self.advance()
            self.add_token(
                TokenType.DOUBLE_STRING if ch == '"' else TokenType.SINGLE_STRING,
                self.source[self.start: self.current].strip(ch)
            )
        elif is_digit(ch):
            while is_digit(self.peek()):
                self.advance()

            if self.peek() == '.':
                self.advance()

                while is_digit(self.peek()):
                    self.advance()

            self.add_token(TokenType.NUMBER, float(self.source[self.start: self.current]))
        elif ch.isalpha():
            while self.peek() and self.peek().isalnum():
                self.advance()

            text = self.source[self.start: self.current]
            if TokenType.has_value(text):
                self.add_token(TokenType(text))
            else:
                self.add_token(TokenType.IDENTIFIER)
        else:
            raise RectaSyntaxError('Unexpected token: ' + ch)

    def is_end(self) -> bool:
        return self.current >= len(self.source)

    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]

    def peek(self) -> str:
        return None if self.is_end() else self.source[self.current]

    def match(self, target: str) -> bool:
        if self.is_end():
            return False
        if self.source[self.current] != target:
            return False

        self.current += 1
        return True

    def add_token(self, token_type: TokenType, literal: Optional[object] = None) -> None:
        self.tokens.append(Token(token_type, self.source[self.start: self.current], literal))


def is_digit(ch: str) -> bool:
    return '0' <= ch <= '9' if ch else False
