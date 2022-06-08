from Expr import Expr
from Stmt import Stmt
from Token import Token
from typing import Any

class FunctionType:
    NONE = "NONE"
    FUNCTION = "FUNCTION"
    INITIALIZER = "INITIALIZER"
    METHOD = "METHOD"

class ClassType:
    NONE = "NONE"
    CLASS = "CLASS"
    SUBCLASS = "SUBCLASS"

class Resolver(Expr.Visitor):
    def __init__(self, interpreter, lox):
        self.interpreter = interpreter
        self.scopes = []
        self.lox = lox
        self.currentFunction = FunctionType.NONE
        self.currentClass = ClassType.NONE

    def visitBlockStmt(self, stmt: Stmt.Block) -> None:
        self.beginScope()
        self.resolveMany(stmt.statements)
        self.endScope()

        return None

    def visitClassStmt(self, stmt: Stmt.Class) -> None:
        enclosingClass = self.currentClass
        self.currentClass = ClassType.CLASS

        self.declare(stmt.name)
        self.define(stmt.name)

        # superclass inherintance
        if stmt.superclass is not None and stmt.name.lexeme == stmt.superclass.name.lexeme:
            self.lox.error(stmt.superclass.name, "A class can't inherit from itself.")

        if stmt.superclass is not None:
            self.currentClass = ClassType.SUBCLASS
            self.resolve(stmt.superclass)

        # inheritance 13.3.2
        if stmt.superclass is not None:
            self.beginScope()
            # peek() in Java is returning top of the stack
            self.scopes[-1]["super"] = True

        self.beginScope()
        # peek() in Java is returning top of the stack
        self.scopes[-1]["this"] = True

        for method in stmt.methods:
            declaration = FunctionType.METHOD
            if method.name.lexeme == "init":
                declaration = FunctionType.INITIALIZER
            self.resolveFunction(method, declaration)

        self.endScope()

        # ending scope if superclass exist
        if stmt.superclass is not None:
            self.endScope()

        self.currentClass = enclosingClass
        return None

    def visitExpressionStmt(self, stmt: Stmt.Expression) -> None:
        self.resolveExpr(stmt.expression)

        return None

    def visitFunctionStmt(self, stmt: Stmt.Function):
        self.declare(stmt.name)
        self.define(stmt.name)
        self.resolveFunction(stmt, FunctionType.FUNCTION)

        return None

    def visitIfStmt(self, stmt: Stmt.If) -> None:
        self.resolveExpr(stmt.condition)
        self.resolveOne(stmt.thenBranch)
        if stmt.elseBranch is not None:
            self.resolveOne(stmt.elseBranch)

        return None

    def visitPrintStmt(self, stmt: Stmt.Print) -> None:
        self.resolveExpr(stmt.expression)
        return None

    def visitReturnStmt(self, stmt: Stmt.Return) -> None:
        if self.currentFunction == FunctionType.NONE:
            self.lox.error(stmt.keyword, "Can't return from top-level code.")

        if stmt.value is not None:
            if self.currentFunction == FunctionType.INITIALIZER:
                self.lox.error(stmt.keyword, "Can't return a value from an initializer.")
            self.resolveExpr(stmt.value)

        return None

    def visitVarStmt(self, stmt: Stmt.Var) -> None:
        self.declare(stmt.name)
        if stmt.initializer is not None:
            self.resolveExpr(stmt.initializer)

        self.define(stmt.name)

        return None

    def visitWhileStmt(self, stmt: Stmt.While) -> None:
        self.resolveExpr(stmt.condition)
        self.resolveMany(stmt.body)

        return None

    def visitAssignExpr(self, expr: Expr.Assign) -> None:
        self.resolveExpr(expr.value)
        self.resolveLocal(expr, expr.name)
        return None

    def visitBinaryExpr(self, expr: Expr.Binary) -> None:
        self.resolveExpr(expr.left)
        self.resolveExpr(expr.right)
        return None

    def visitCallExpr(self, expr: Expr.Call) -> None:
        self.resolveExpr(expr.callee)
        for arg in expr.arguments:
            self.resolveExpr(arg)

        return None

    def visitGetExpr(self, expr: Expr.Get) -> None:
        self.resolve(expr.object)
        return None

    def visitGroupingExpr(self, expr: Expr.Grouping) -> None:
        self.resolveExpr(expr.expression)
        return None

    def visitLiteralExpr(self, expr: Expr.Literal) -> None:
        return None

    def visitLogicalExpr(self, expr: Expr.Logical) -> None:
        self.resolveExpr(expr.left)
        self.resolveExpr(expr.right)
        return None

    def visitSetExpr(self, expr: Expr.Set) -> None:
        self.resolve(expr.value)
        self.resolve(expr.object)
        return None

    def visitSuperExpr(self, expr: Expr.Super) -> None:
        if self.currentClass == ClassType.NONE:
            self.lox.error(expr.keyword, "Can't use 'super' outside of a class.")
        elif self.currentClass != ClassType.SUBCLASS:
            self.lox.error(expr.keyword, "Can't use 'super' in a class with no superclass.")

        self.resolveLocal(expr, expr.keyword)
        return None

    def visitThisExpr(self, expr: Expr.This) -> None:
        if self.currentClass == ClassType.NONE:
            self.lox.error(expr.keyword, "Can't use 'this' outside of a class.")
            return None

        self.resolveLocal(expr, expr.keyword)
        return None

    def visitUnaryExpr(self, expr: Expr.Unary) -> None:
        self.resolveExpr(expr.right)
        return None

    def visitVariableExpr(self, expr: Expr.Variable):
        # peek() in Java is returning top of the stack
        if self.scopes and self.scopes[-1].get(expr.name.lexeme) is False:
            self.lox.error(expr.name, "Can't read local variable in its own initialzier.")

        self.resolveLocal(expr, expr.name)
        return None

    def resolve(self, object: Any):
        if isinstance(object, list):
            self.resolveMany(object)
        elif isinstance(object, tuple(Stmt.all_inner_class())):
            self.resolveOne(object)
        elif isinstance(object, tuple(Expr.all_inner_class())):
            self.resolveExpr(object)


    def resolveMany(self, statements: list[Stmt]) -> None:
        for statement in statements:
            self.resolveOne(statement)

    def resolveOne(self, stmt: Stmt) -> None:
        stmt.accept(self)

    def resolveExpr(self, expr: Expr):
        expr.accept(self)

    def resolveFunction(self, function: Stmt.Function, type: FunctionType):
        enclosingFunction = self.currentFunction
        self.currentFunction = type
        self.beginScope()
        for param in function.params:
            self.declare(param)
            self.define(param)

        self.resolve(function.body)
        self.endScope()

        self.currentFunction = enclosingFunction

    def beginScope(self):
        self.scopes.append({})

    def endScope(self):
        self.scopes.pop(-1)

    def declare(self, name: Token) -> None:
        if not self.scopes:
            return None

        # peek() in Java is returning top of the stack
        scope = self.scopes[-1]

        if name.lexeme in scope:
            self.lox.error(name, "Already a variable with this name in this scope.")

        scope[name.lexeme] = False

    def define(self, name: Token) -> None:
        if not self.scopes:
            return None
        # peek() in Java is returning top of the stack
        self.scopes[-1][name.lexeme] = True

    def resolveLocal(self, expr: Expr, name: Token):
        for i in reversed(range(len(self.scopes))):
            if self.scopes[i].get(name.lexeme):
                self.interpreter.resolve(expr, len(self.scopes) - 1 - i)
                return
