from Token import Token
from LoxRuntimeError import LoxRuntimeError
from typing import Any


class LoxInstance:
    def __init__(self, klass):
        self.klass = klass
        self.fields = {}

    def __str__(self):
        return self.klass.name + " instance"

    def get(self, name: Token):
        if self.fields.get(name.lexeme):
            return self.fields.get(name.lexeme)

        method = self.klass.findMethod(name.lexeme)
        if method is not None:
            return method.bind(self)

        raise LoxRuntimeError(name, "Undefined property '" + name.lexeme + "'.")

    def set(self, name: Token, value: Any):
        self.fields[name.lexeme] = value
