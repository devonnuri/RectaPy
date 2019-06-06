from typing import Optional

from rectapy import TokenType


class Token:
    def __init__(self, token_type: TokenType, lexeme: str, literal: Optional[object] = None):
        self.type: TokenType = token_type
        self.lexeme: str = lexeme
        self.literal: Optional[object] = literal

    def __str__(self):
        return f'{self.type.name} {self.lexeme} {self.literal or ""}'
