from LoxCallable import LoxCallable
from LoxInstance import LoxInstance
from LoxFunction import LoxFunction
from typing import Any, List, Optional


class LoxClass(LoxCallable):
    def __init__(self, name: str, superclass, methods: dict) -> None:
        self.superclass = superclass
        self.name = name
        self.methods = methods

    def __str__(self) -> str:
        return self.name

    def findMethod(self, name: str) -> Optional[LoxFunction]:
        if self.methods.get(name):
            return self.methods.get(name)

        if self.superclass is not None:
            return self.superclass.findMethod(name)

        return None

    def call(self, interpreter, arguments: List[Any]) -> LoxInstance:
        instance = LoxInstance(self)
        initializer = self.findMethod("init")
        if initializer is not None:
            initializer.bind(instance).call(interpreter, arguments)

        return instance

    def arity(self) -> int:
        initializer = self.findMethod("init")
        if initializer is None:
            return 0

        return initializer.arity()
