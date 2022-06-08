from typing import Any, Optional

from LoxRuntimeError import LoxRuntimeError
from Token import Token


class Environment:
    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = None
        if enclosing:
            self.enclosing = enclosing # is an Environemnt instance

    def get(self, name: Token) -> Any:
        if name.lexeme in self.values:
            return self.values.get(name.lexeme)

        if self.enclosing is not None:
            return self.enclosing.get(name)

        raise LoxRuntimeError(name, "Undefined variable '" + name.lexeme + "'.")

    def define(self, name: str, value: Any) -> None:
        self.values[name] = value

    def ancestor(self, distance: int):
        environment = self
        for i in range(distance):
            environment = environment.enclosing

        return environment

    def getAt(self, distance: int, name: str) -> Any:
        return self.ancestor(distance).values.get(name)

    def assignAt(self, distance: int, name: Token, value: Any) -> None:
        self.ancestor(distance).values[name.lexeme] = value

    def assign(self, name: Token, value: Any) -> None:
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return

        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return

        raise LoxRuntimeError(name, "Undefined variable '" + name.lexeme + "'.")
