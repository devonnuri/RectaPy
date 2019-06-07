from typing import Optional

from rectapy import TokenType


class Token:
    def __init__(self, token_type: TokenType, lexeme: str, literal: Optional[object] = None):
        self.type = token_type
        self.lexeme = lexeme
        self.literal = literal

    def __str__(self):
        return f'{self.type.name} {self.lexeme} {self.literal or ""}'
