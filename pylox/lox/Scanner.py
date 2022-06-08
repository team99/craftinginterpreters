from typing import Optional

from Token import Token
from TokenType import TokenType

class Scanner():
    KEYWORDS = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "fun": TokenType.FUN,
        "for": TokenType.FOR,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE,
    }

    def __init__(self, source: str, lox):
        self.lox = lox
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

    def scanTokens(self) -> list[Token]:
        while not self.isAtEnd():
            # We are at the beginning of the next lexeme
            self.start = self.current
            self.scanToken()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scanToken(self) -> None:
        c = self.advance()
        if c == "(":
            self.addToken(TokenType.LEFT_PAREN)
        elif c == ")":
            self.addToken(TokenType.RIGHT_PAREN)
        elif c == "{":
            self.addToken(TokenType.LEFT_BRACE)
        elif c == "}":
            self.addToken(TokenType.RIGHT_BRACE)
        elif c == ",":
            self.addToken(TokenType.COMMA)
        elif c == ".":
            self.addToken(TokenType.DOT)
        elif c == "-":
            self.addToken(TokenType.MINUS)
        elif c == "+":
            self.addToken(TokenType.PLUS)
        elif c == ";":
            self.addToken(TokenType.SEMICOLON)
        elif c == "*":
            self.addToken(TokenType.STAR)

        # operators
        elif c == "!":
            self.addToken(TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG)
        elif c == "=":
            self.addToken(TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL)
        elif c == "<":
            self.addToken(TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS)
        elif c == ">":
            self.addToken(TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER)

        # comments
        elif c == "/":
            if self.match("/"):
                # A comment goes until the end of the line.
                while self.peek() != "/n" and not self.isAtEnd():
                    self.advance()
            else:
                self.addToken(TokenType.SLASH)

        # whitespaces
        elif c == " ":
            pass
        elif c == "\r":
            pass
        elif c == "\t":
            # Ignore whitespace
            pass
        elif c == "\n":
            self.line += 1

        # string literals
        elif c == '"':
            self.string()

        else:
            # number literals
            if self.isDigit(c):
                self.number()
            # reserved number and identifier
            elif self.isAlpha(c):
                self.identifier()
            else:
                self.lox.error(self.line, "Unexpected character.")

    def identifier(self) -> None:
        while self.isAlphaNumeric(self.peek()):
            self.advance()

        text = self.source[self.start:self.current]
        type = self.KEYWORDS.get(text)
        if type is None:
            type = TokenType.IDENTIFIER

        self.addToken(type)

    def string(self) -> None:
        while self.peek() != '"' and not self.isAtEnd():
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        if self.isAtEnd():
            self.lox.error(self.line, "Unterminated string.")

        # The closing ".
        self.advance()

        # Trim the surrounding quotes.
        value = self.source[self.start + 1: self.current - 1]
        self.addTokenLiteral(TokenType.STRING, value)

    def number(self) -> None:
        while self.isDigit(self.peek()):
            self.advance()

        # Look for fractional part
        if self.peek() == "." and self.isDigit(self.peekNext()):
            # Consume the "."
            self.advance()

            while self.isDigit(self.peek()):
                self.advance()

        value = float(self.source[self.start:self.current])
        self.addTokenLiteral(TokenType.NUMBER, value)

    def match(self, expected: str) -> bool:
        if self.isAtEnd():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def peek(self) -> str:
        if self.isAtEnd():
            return ""
        current_char = self.source[self.current]
        return current_char

    def peekNext(self) -> str:
        if self.current + 1 >= len(self.source):
            return ""
        return self.source[self.current + 1]

    def isAlpha(self, c:str) -> bool:
        return (c >= "a" and c <= "z") or (c >= "A" and c <= "Z") or c == "_"

    def isAlphaNumeric(self, c: str) -> bool:
        return self.isAlpha(c) or self.isDigit(c)

    def isDigit(self, c: str) -> bool:
        return c >= "0" and c <= "9"

    def isAtEnd(self) -> bool:
        return self.current >= len(self.source)

    def advance(self) -> str:
        current_char = self.source[self.current]
        self.current += 1
        return current_char

    def addToken(self, type: str) -> None:
        self.addTokenLiteral(type, None)

    def addTokenLiteral(self, type: str, literal: Optional[str]) -> None:
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))
