from abc import ABC, abstractmethod
from typing import Any, List


class Callable(ABC):
    @abstractmethod
    def arity(self) -> int:
        pass

    @abstractmethod
    def call(self, interpreter, arguments: List[Any]):
        pass
