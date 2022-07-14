from __future__ import annotations

from typing import Dict, Any, Optional

from rectapy import Token, RectaRuntimeError


class Environment:
    def __init__(self, enclosing: Optional[Environment] = None):
        self.values: Dict[str, Any] = {}
        self.enclosing = enclosing

    def define(self, key: str, value: Any) -> None:
        self.values[key] = value

    def ancestor(self, distance: int):
        environment = self
        for i in range(distance):
            environment = environment.enclosing

        return environment

    def get_at(self, distance: int, name: str):
        return self.ancestor(distance).values[name]

    def assign(self, key: Token, value: Any):
        if key.lexeme in self.values:
            self.values[key.lexeme] = value

        if self.enclosing:
            self.enclosing.assign(key, value)

        raise RectaRuntimeError(f'Undefined variable \'{key.lexeme}\'.')

    def assign_at(self, distance: int, name: Token, value: Any):
        self.ancestor(distance).values[name.lexeme] = value

    def get(self, key: Token):
        if key.lexeme in self.values:
            return self.values[key.lexeme]

        if self.enclosing is not None:
            return self.enclosing.get(key)

        raise RectaRuntimeError(f'Undefined variable \'{key.lexeme}\'.')

