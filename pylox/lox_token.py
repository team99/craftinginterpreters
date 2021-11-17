from dataclasses import dataclass
from typing import Any

from .lox_token_type import TokenType

keywords = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "for": TokenType.FOR,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "fun": TokenType.FUN,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "this": TokenType.THIS,
    "super": TokenType.SUPER,
    "true": TokenType.TRUE,
    "while": TokenType.WHILE,
    "var": TokenType.VAR,
}


@dataclass
class Token:
    type: TokenType
    lexeme: str
    literal: Any
    line: int

    def __str__(self):
        return f"{self.type} {self.lexeme} {self.literal}"
