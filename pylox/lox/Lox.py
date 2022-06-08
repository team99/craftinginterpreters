import sys

from Scanner import Scanner
from Parser import Parser
from AstPrinter import AstPrinter
from Token import Token
from TokenType import TokenType
from Interpreter import Interpreter
from LoxRuntimeError import LoxRuntimeError
from Resolver import Resolver

class Lox:
    def __init__(self):
        self.hadError = False
        self.hadRuntimeError = False
        self.interpreter = Interpreter(self)

    def main(self, args: list) -> None:
        if len(args) > 1:
            print("Usage: jlox [script]")
            sys.exit(64)
        elif len(args) == 1:
            self.runFile(args[0])
        else:
            self.runPrompt()

    def runFile(self, path: str) -> None:
        with open(path, "r") as f:
            bytes = f.read()
        self.run(bytes)

        # Indicate an error in the exit code.
        if self.hadError:
            sys.exit(65)
        if self.hadRuntimeError:
            sys.exit(70)

    def runPrompt(self) -> None:
        while True:
            print("> ", end="")
            line = input()
            if line.rstrip("\n") == "":
                print("Goodbye!")
                break
            self.run(line)
            self.hadError = False

    def run(self, source) -> None:
        scanner = Scanner(source, self)
        tokens = scanner.scanTokens()

        parser = Parser(tokens, self)
        statements = parser.parse()

        # stop if there was a syntax error
        if self.hadError:
            return

        resolver = Resolver(self.interpreter, self)
        resolver.resolve(statements)

        if self.hadError:
            return

        self.interpreter.interpret(statements)

        """
        print(AstPrinter().print_(expression))
        """

        # For now, just print the tokens.
        """
        for token in tokens:
            print(token)
            """

    def error(self, line: int, message: str) -> None:
        self.report(line, "", message)

    def errorToken(self, token: Token, message: str) -> None:
        if token.type == TokenType.EOF:
            self.report(token.line, " at end", message)
        else:
            self.report(token.line, " at " + token.lexeme + "'", message)

    def runtimeError(self, error: LoxRuntimeError):
        print(str(error) + "\n[line " + str(error.token.line) + "]")
        self.hadRuntimeError = True

    def report(self, line: int, where: str, message: str):
        print("[line " + str(line) + "] Error" + where + ": " + message)
        self.hadError = True


def argParse():
    args = sys.argv
    args = args[1:]
    return args


if __name__ == "__main__":
    args = argParse()
    app = Lox()
    app.main(args)
