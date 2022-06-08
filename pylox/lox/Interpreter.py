from typing import Any
import time

from Token import Token
from TokenType import TokenType
from Expr import Expr
from Environment import Environment
from Stmt import Stmt
from LoxRuntimeError import LoxRuntimeError
from LoxCallable import LoxCallable
from LoxClass import LoxClass
from LoxFunction import LoxFunction
from LoxInstance import LoxInstance
from Return import Return


class ClockCallable(LoxCallable):
    def arity(self) -> int:
        return 0

    def call(self, interpreter, arguments):
        return time.time()

    def __str__(self):
        return "<native fn>"

class Interpreter(Expr.Visitor, Stmt.Visitor):
    def __init__(self, lox):
        self.lox = lox
        self.globals = Environment()
        self.environment = self.globals
        self.locals = {}

        self.globals.define("clock", ClockCallable())

    def visitLiteralExpr(self, expr: Expr.Literal) -> Any:
        return expr.value

    def visitLogicalExpr(self, expr: Expr.Logical) -> Any:
        left = self.evaluate(expr.left)

        if expr.operator.type == TokenType.OR:
            if self.isTruthy(left):
                return left
        else:
            if not self.isTruthy(left):
                return left

        return self.evaluate(expr.right)

    def visitSetExpr(self, expr: Expr.Set) -> Any:
        object = self.evaluate(expr.object)
        if not isinstance(object, LoxInstance):
            raise LoxRuntimeError(expr.name, "Only instances have fields.")

        value = self.evaluate(expr.value)
        object.set(expr.name, value)
        return value

    def visitSuperExpr(self, expr: Expr.Super) -> Any:
        distance = self.locals.get(expr)
        superclass = self.environment.getAt(distance, "super")

        object = self.environment.getAt(distance - 1, "this")

        method = superclass.findMethod(expr.method.lexeme)

        if method is None:
            raise LoxRuntimeError(expr.method, "Undefined property '" + expr.method.lexeme + "'.")
        return method.bind(object)

    def visitThisExpr(self, expr: Expr.This) -> Any:
        return self.lookUpVariable(expr.keyword, expr)

    def visitUnaryExpr(self, expr: Expr.Unary) -> Any:
        right = self.evaluate(expr.right)

        if expr.operation.type == TokenType.MINUS:
            self.checkNumberOperand(expr.operator, right);
            return -right
        elif expr.operation.type == TokenType.BANG:
            return not self.isTruthy(right)

        # Unreachable
        return None

    def visitVariableExpr(self, expr: Expr.Variable) -> Any:
        return self.lookUpVariable(expr.name, expr)

    def lookUpVariable(self, name: Token, expr: Expr) -> Any:
        distance = self.locals.get(expr)
        if distance is not None:
            return self.environment.getAt(distance, name.lexeme)
        else:
            return self.globals.get(name)

    def checkNumberOperand(self, operator: Token, operand: Any) -> None:
        if isinstance(operand, float):
            return
        raise LoxRuntimeError(operator, "Operand must be a number")

    def checkNumberOperands(self, operator: Token, left: Any, right: Any) -> None:
        if isinstance(left, float) and isinstance(right, float):
            return
        raise LoxRuntimeError(operator, "Operands must be two numbers or two strings")

    def isTruthy(self, object: Any) -> bool:
        if object is None:
            return False
        if isinstance(object, bool):
            return object

        return True

    def isEqual(self, a: Any, b: Any) -> bool:
        if a is None and b is None:
            return True
        if a is None:
            return False

        return a == b

    def stringify(self, object: Any) -> str:
        if object is None:
            return "nil"

        if object is True:
            return "true"
        if object is False:
            return "false"

        if isinstance(object, float):
            text = str(object)
            if text.endswith(".0"):
                text = text[0:len(text) - 2]

            return text

        return str(object)

    def visitGroupingExpr(self, expr: Expr.Grouping) -> Any:
        return self.evaluate(expr.expression)

    def evaluate(self, expr: Expr) -> Any:
        return expr.accept(self)

    def visitBinaryExpr(self, expr: Expr.Binary) -> Any:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        # comparison
        if expr.operator.type == TokenType.GREATER:
            self.checkNumberOperands(expr.operator, left, right);
            return left > right
        if expr.operator.type == TokenType.GREATER_EQUAL:
            self.checkNumberOperands(expr.operator, left, right);
            return left >= right
        if expr.operator.type == TokenType.LESS:
            self.checkNumberOperands(expr.operator, left, right);
            return left < right
        if expr.operator.type == TokenType.LESS_EQUAL:
            self.checkNumberOperands(expr.operator, left, right);
            return left <= right

        # equality
        if expr.operator.type == TokenType.BANG_EQUAL:
            return not self.isEqual(left, right)
        if expr.operator.type == TokenType.EQUAL_EQUAL:
            return self.isEqual(left, right)

        # term
        if expr.operator.type == TokenType.MINUS:
            self.checkNumberOperands(expr.operator, left, right);
            return left - right
        if expr.operator.type == TokenType.PLUS:
            # Can be number of text
            if isinstance(left, float) and isinstance(right, float):
                return left + right
            if isinstance(left, str) and isinstance(right, str):
                return left + right
        if expr.operator.type == TokenType.SLASH:
            self.checkNumberOperands(expr.operator, left, right);
            return left / right
        if expr.operator.type == TokenType.STAR:
            self.checkNumberOperands(expr.operator, left, right);
            return left * right

        # Unreachable
        return None

    def visitCallExpr(self, expr: Expr.Call) -> Any:
        callee = self.evaluate(expr.callee)

        arguments = []
        for argument in expr.arguments:
            arguments.append(self.evaluate(argument))

        if not isinstance(callee, LoxCallable):
            raise LoxRuntimeError(expr.paren, "Can only call functions and classes.")

        function = callee

        if len(arguments) != function.arity():
            raise LoxRuntimeError(expr.paren, "Expected " + str(function.arity()) + " arguments but got " + str(len(arguments)) + ".")

        return function.call(self, arguments)

    def visitGetExpr(self, expr: Expr.Get) -> Any:
        object = self.evaluate(expr.object)
        if isinstance(object, LoxInstance):
            return object.get(expr.name)

        raise LoxRuntimeError(expr.name, "Only instances have properties.")

    def visitExpressionStmt(self, stmt: Stmt.Expression) -> None:
        self.evaluate(stmt.expression)
        return None

    def visitFunctionStmt(self, stmt: Stmt.Function) -> None:
        function = LoxFunction(stmt, self.environment, False)
        self.environment.define(stmt.name.lexeme, function)
        return None

    def visitIfStmt(self, stmt: Stmt.If) -> None:
        if self.isTruthy(self.evaluate(stmt.condition)):
            self.execute(stmt.thenBranch)
        elif stmt.elseBranch is not None:
            self.execute(stmt.elseBranch)
        return None

    def visitPrintStmt(self, stmt: Stmt.Expression) -> None:
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))
        return None

    def visitReturnStmt(self, stmt: Stmt.Return) -> None:
        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)

        raise Return(value)

    def visitVarStmt(self, stmt: Stmt.Var) -> None:
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)

        self.environment.define(stmt.name.lexeme, value)
        return None

    def visitWhileStmt(self, stmt: Stmt.While) -> None:
        while self.isTruthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)
        return None

    def visitAssignExpr(self, expr: Expr.Assign) -> Any:
        value = self.evaluate(expr.value)

        distance = self.locals.get(expr)
        if distance is not None:
            self.environment.assignAt(distance, expr.name, value)
        else:
            self.globals.assign(expr.name, value)
        return value

    def execute(self, stmt: Stmt) -> None:
        stmt.accept(self)

    def resolve(self, expr: Expr, depth: int) -> None:
        self.locals[expr] = depth

    def executeBlock(self, statements: list[Stmt], environment: Environment) -> None:
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    def visitBlockStmt(self, stmt: Stmt.Block) -> None:
        self.executeBlock(stmt.statements, Environment(self.environment))
        return None

    def visitClassStmt(self, stmt: Stmt.Class) -> None:
        # evaluate superclass
        superclass = None
        if stmt.superclass is not None:
            superclass = self.evaluate(stmt.superclass)
            if not isinstance(superclass, LoxClass):
                raise LoxRuntimeError(stmt.superclass.name, "Superclass must be a class.")

        self.environment.define(stmt.name.lexeme, None)

        if stmt.superclass is not None:
            self.environment = Environment(self.environment)
            self.environment.define("super", superclass)

        methods = {}
        for method in stmt.methods:
            function = LoxFunction(method, self.environment, method.name.lexeme == "init")
            methods[method.name.lexeme] = function

        klass = LoxClass(stmt.name.lexeme, superclass, methods)

        if superclass is not None:
            self.environment = self.environment.enclosing

        self.environment.assign(stmt.name, klass)
        return None

    def interpret(self, statements: list[Stmt]) -> None:
        for statement in statements:
            value = self.execute(statement)
        """
        try:
            for statement in statements:
                value = self.execute(statement)
        except LoxRuntimeError as e:
            self.lox.runtimeError(e)
            """
