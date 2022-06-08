from Expr import Expr
from Token import Token
from TokenType import TokenType

class AstPrinter(Expr.Visitor):
    def print_(self, expr: Expr):
        return expr.accept(self)

    def visitBinaryExpr(self, expr: Expr.Binary):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visitGroupingExpr(self, expr: Expr.Grouping):
        return self.parenthesize("group", expr.expression)

    def visitLiteralExpr(self, expr: Expr.Literal):
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visitUnaryExpr(self, expr: Expr.Unary):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name: str, *exprs):
        builder = []
        builder.append("(")
        builder.append(name)

        for expr in exprs:
            builder.append(" ")
            builder.append(expr.accept(self))

        builder.append(")")
        return "".join(builder)

    def main(self):
        expression = Expr.Binary(
            Expr.Unary(
                Token(TokenType.MINUS, "-", None, 1),
                Expr.Literal(123)
            ),
            Token(TokenType.STAR, "*", None, 1),
            Expr.Grouping(
                Expr.Literal(45.67)
            ),
        )
        print(self.print_(expression))

if __name__ == "__main__":
    app = AstPrinter()
    app.main()
