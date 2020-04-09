# TOKENS

PROGRAM = 'PROGRAM'
MINUS = 'MINUS'
PLUS = 'PLUS'
DIV = 'DIV'
MUL = 'MUL'
BEGIN = 'BEGIN'
END = 'END'
VAR = 'VAR'
INTEGER = 'INTEGER'
ASSIGN = 'ASSIGN'
REAL = 'REAL'
ID = 'ID'
DOT = 'DOT'
EOF = 'EOF'
INTEGER_CONST = 'INTEGER_CONST'
REAL_CONST = 'REAL_CONST'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
SEMI = 'SEMI'
COLON = 'COLON'
COMMA = 'COMMA'
INTEGER_DIV = 'INTEGER_DIV'
FLOAT_DIV = 'FLOAT_DIV'


# Token class
class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type},{value})'.format(type=self.type, value=self.value)

    def __repr__(self):
        return self.__str__()


# reserved words
RESERVED_KEYWORDS = {
    "PROGRAM": Token(PROGRAM, PROGRAM),
    "VAR": Token(VAR, VAR),
    "DIV": Token(DIV, DIV),
    "INTEGER": Token(INTEGER, INTEGER),
    "REAL": Token(REAL, REAL),
    "BEGIN": Token(BEGIN, BEGIN),
    "END": Token(END, END)
}


# Lexer class

class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = text[self.pos]

    def skip_whitespace(self):
        while self.current_char.isspace():
            self.advance()

    def advance(self):
        if ++self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_comment(self):
        while self.current_char != '}':
            self.advance()

    def get_ID(self):

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
            if self.current_char == '{':
                self.skip_comment()
            if self.current_char.isalpha():
                return self.get_ID()
