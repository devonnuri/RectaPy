from __future__ import annotations

from typing import Dict, Any, Optional

from rectapy import Token, RuntimeError


class Environment:
    def __init__(self, enclosing: Optional[Environment] = None):
        self.values: Dict[str, Any] = {}
        self.enclosing = enclosing

    def define(self, key: str, value: Any) -> None:
        self.values[key] = value

    def assign(self, key: Token, value: Any) -> None:
        if key.lexeme in self.values:
            self.values[key.lexeme] = value
            return

        if self.enclosing is not None:
            self.enclosing.assign(key, value)
            return

        raise RuntimeError(f'Undefined variable \'{key.lexeme}\'.')

    def get(self, key: Token) -> Any:
        if key.lexeme in self.values:
            return self.values[key.lexeme]

        if self.enclosing is not None:
            return self.enclosing.get(key)

        raise RuntimeError(f'Undefined variable \'{key.lexeme}\'.')

