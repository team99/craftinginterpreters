from Stmt import Stmt
from LoxCallable import LoxCallable
from Environment import Environment
from Return import Return


class LoxFunction(LoxCallable):
    def __init__(self, declaration: Stmt.Function, closure: Environment, isInitializer: bool):
        self.declaration = declaration
        self.closure = closure
        self.isInitializer = isInitializer

    def bind(self, instance):
        """
        binding 'this' method into the instance
        """
        environment = Environment(self.closure)
        environment.define("this", instance)
        return LoxFunction(self.declaration, environment, self.isInitializer)

    def call(self, interpreter, arguments):
        """
        execute the Lox function declaration body
        """
        environment = Environment(self.closure)
        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme, arguments[i])

        try:
            interpreter.executeBlock(self.declaration.body, environment)
        except Return as returnValue:
            if self.isInitializer:
                return self.closure.getAt(0, "this")
            return returnValue.value

        if self.isInitializer:
            return self.closure.getAt(0, "this")

        return None

    def arity(self):
        """
        return the number of declared params
        """
        return len(self.declaration.params)

    def __str__(self):
        return "<fn " + self.declaration.name.lexeme + ">"
