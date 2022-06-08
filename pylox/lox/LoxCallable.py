from typing import Any
from Expr import Expr

class LoxCallable:

    def arity(self) -> int:
        raise NotImplementedError

    def call(self, interpreter, arguments: list[Any]):
        raise NotImplementedError
