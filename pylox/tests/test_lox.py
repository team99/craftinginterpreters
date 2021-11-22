import pytest

from pylox import lox
from pylox.lox_token import Token
from pylox.lox_token_type import TokenType


@pytest.fixture
def eof():
    return "pylox/tests/test_source_files/01_empty.lox"


def test_eof(eof):
    expected = [Token(TokenType.EOF, lexeme="", literal=None, line=1)]
    assert lox.main(eof) == expected


@pytest.fixture
def numbers():
    return "pylox/tests/test_source_files/02_numbers.lox"


def test_numbers(numbers):
    expected = [
        Token(TokenType.NUMBER, lexeme="1", literal="1", line=1),
        Token(TokenType.EOF, lexeme="", literal=None, line=2),
    ]
    assert lox.main(numbers) == expected


@pytest.fixture
def print_number():
    return "pylox/tests/test_source_files/03_print.lox"


def test_print_numbers(print_number):
    expected = [
        Token(TokenType.PRINT, lexeme="print", literal=None, line=1),
        Token(TokenType.NUMBER, lexeme="1", literal="1", line=1),
        Token(TokenType.SEMICOLON, lexeme=";", literal=None, line=1),
        Token(TokenType.EOF, lexeme="", literal=None, line=2),
    ]
    assert lox.main(print_number) == expected


@pytest.fixture
def print_multiple():
    return "pylox/tests/test_source_files/04_multiple_print.lox"


def test_multiple(print_multiple):
    expected = [
        Token(TokenType.PRINT, lexeme="print", literal=None, line=1),
        Token(TokenType.NUMBER, lexeme="1", literal="1", line=1),
        Token(TokenType.SEMICOLON, lexeme=";", literal=None, line=1),
        Token(TokenType.PRINT, lexeme="print", literal=None, line=2),
        Token(TokenType.NUMBER, lexeme="2", literal="2", line=2),
        Token(TokenType.SEMICOLON, lexeme=";", literal=None, line=2),
        Token(TokenType.PRINT, lexeme="print", literal=None, line=4),
        Token(TokenType.NUMBER, lexeme="3", literal="3", line=4),
        Token(TokenType.SEMICOLON, lexeme=";", literal=None, line=4),
        Token(TokenType.EOF, lexeme="", literal=None, line=6),
    ]
    assert lox.main(print_multiple) == expected
