from TokenType import TokenType

class Token:
    def __init__(self, type: str, lexeme: str, literal, line: int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return f"{self.type} {self.lexeme} {self.literal}"
