import logging
import sys
from dataclasses import dataclass, field
from typing import Any

from .lox_token import Token, keywords
from .lox_token_type import TokenType

# we use this to ensure we don't try to execute that
# has a known error
# it also lets us exit with a non-zero exit code
# if had_error, sys.exit(65)
had_error = False

logging.basicConfig(
    format="%(asctime)s %(levelgname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


def throw_error(line: int, message: str):
    report_error(line, message)


def report_error(line: int, message: str):
    logging.error(f"{line}: {message}")
    # had_error = True


TOKENS_AND_TYPES = {
    "(": TokenType.LEFT_PAREN,
    ")": TokenType.RIGHT_PAREN,
    "{": TokenType.LEFT_BRACE,
    "}": TokenType.RIGHT_BRACE,
    ",": TokenType.COMMA,
}


@dataclass
class Scanner:
    source: str
    tokens: list[Token] = field(default_factory=list)
    start: int = 0
    current: int = 0
    line: int = 1

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def scan_token(self) -> None:
        c = self.advance()
        if c in TOKENS_AND_TYPES:
            self.add_token(TOKENS_AND_TYPES.get(c))

        elif c == ".":
            self.add_token(TokenType.DOT)
        elif c == "-":
            self.add_token(TokenType.MINUS)
        elif c == "+":
            self.add_token(TokenType.PLUS)
        elif c == ";":
            self.add_token(TokenType.SEMICOLON)
        elif c == "/":
            if self.match("/"):
                # A comment goes until the end of the line.
                while self.peek() != "\n" and not self.is_at_end():
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)
        elif c == "*":
            self.add_token(TokenType.STAR)
        elif c == "!":
            self.add_token(TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG)
        elif c == "=":
            self.add_token(
                TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL
            )
        elif c == "<":
            self.add_token(TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS)
        elif c == ">":
            self.add_token(
                TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER
            )
        elif c in {" ", "\r", "\t"}:
            # ignore whitespace.
            pass
        elif c == "\n":
            self.line += 1
        elif c == '"':
            self.string()
        elif c.isdigit():
            self.number()
        elif c.isalpha():
            self.identifier()
        else:
            throw_error(self.line, f"Unexpected character {c}")

    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, token_type: TokenType, literal: Any = None) -> None:
        text = self.source[self.start : self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False

        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def peek(self) -> str:
        if self.is_at_end():
            return "\0"

        return self.source[self.current]

    def string(self) -> None:
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()
        if self.is_at_end():
            throw_error(self.line, "Unterminated string.")
            return
        self.advance()

        value = self.source[self.start + 1 : self.current - 1]
        self.add_token(TokenType.STRING, value)

    def number(self) -> None:
        while self.peek().isdigit():
            self.advance()
        if self.peek() == "." and self.peek_next().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()
        self.add_token(TokenType.NUMBER, self.source[self.start : self.current])

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"

        return self.source[self.current + 1]

    def identifier(self) -> None:
        while self.peek().isalnum():
            self.advance()

        text = self.source[self.start : self.current]
        token_type = keywords.get(text)
        if not token_type:
            token_type = TokenType.IDENTIFIER

        self.add_token(token_type)


def run(lines: str, return_tokens: bool = False):
    scanner = Scanner(lines)
    tokens = scanner.scan_tokens()

    if return_tokens:
        return tokens

    for token in tokens:
        print(token)


def exit():
    raise SystemExit("Usage: python3 -m pylox.lox [script]")


def main(filename: str, return_tokens: bool = True):
    if not filename:
        exit()

    with open(filename) as file:
        text = file.read()
        tokens = run(text, return_tokens)
        if tokens:
            return tokens


if __name__ == "__main__":
    if len(sys.argv) != 2:
        exit()

    # TODO to add run prompt
    main(sys.argv[1], return_tokens=False)
