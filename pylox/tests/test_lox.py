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
