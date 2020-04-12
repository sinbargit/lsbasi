# TOKENS

PROGRAM = 'PROGRAM'
MINUS = 'MINUS'
PLUS = 'PLUS'
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
    "DIV": Token(INTEGER_DIV, 'DIV'),
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

    def error(self):
        raise Exception('lexer error')

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
        r = ''
        while self.current_char.isalpha():
            r += self.current_char
            self.advance()
        reserve = RESERVED_KEYWORDS.get(r)
        if reserve is not None:
            return reserve
        else:
            return Token(ID, r)

    def integer(self):
        r = ''
        real = False
        while self.current_char.isdigit() or self.current_char == '.':
            r += self.current_char
            if self.current_char == '.':
                if real:
                    self.error()
                else:
                    real = True
            self.advance()
        if real:
            return Token(REAL_CONST, r)
        return Token(INTEGER_CONST, r)

    def peek(self, value):
        return self.text[self.pos + 1] == value

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
            if self.current_char == '{':
                self.skip_comment()
            if self.current_char.isalpha():
                return self.get_ID()
            if self.current_char.isdigit():
                return self.integer()
            if self.current_char == '+':
                return Token(PLUS, '+')
            if self.current_char == '-':
                return Token(MINUS, '-')
            if self.current_char == '*':
                return Token(MUL, '*')
            if self.current_char == '.':
                return Token(DOT, '.')
            if self.current_char == ':' and self.peek('='):
                return Token(ASSIGN, ':=')
            if self.current_char == '/':
                return Token(REAL, '/')
            if self.current_char == '(':
                return Token(LPAREN, '(')
            if self.current_char == ')':
                return Token(RPAREN, ')')
            if self.current_char == ':':
                return Token(COLON, ':')
            if self.current_char == ',':
                return Token(COMMA, ',')
            if self.current_char == ';':
                return Token(SEMI, ';')

        return Token(EOF, EOF)


# AST NODE

class AST(object):
    pass


class Program(AST):
    def __init__(self, name, block):
        self.name = name
        self.block = block


class Block(AST):
    def __init__(self, declarations, compound_statements):
        self.declarations = declarations
        self.compound_statements = compound_statements


class Declaration(AST):
    def __init__(self, ID, type):
        self.ID = ID
        self.type = type


class Compound(AST):
    def __init__(self, statelment_list):
        self.statement_list = statelment_list


class Assign(AST):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class BinOp(AST):
    def __init__(self, left, op, right):
        self.token = self.op = op
        self.left = left
        self.right = right


class Variable(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Type(AST):
    def __init__(self, value):
        self.value = value


# Parse
class Parse(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('parse error')

    def eat(self, type):
        if self.current_token.type != type:
            self.error()
        else:
            self.current_token = self.lexer.get_next_token()

    def variable(self):
        """variable: ID"""
        var = Variable(self.current_token)
        self.eat(ID)
        return var

    def declaration(self):
        """variable |(COMMA variable)+ COLON type"""
        temp = [self.current_token]
        self.eat(ID)
        while self.current_token.type == COMMA:
            temp.append(self.current_token)
        self.eat(COLON)
        type_node = Type(self.current_token)
        self.eat(self.current_token.type)
        self.eat(SEMI)
        list = [Declaration(Variable(var), type_node) for var in temp]
        return list

    def declarations(self):
        """declarations: VAR (declaration SEMI)+ | empty"""
        self.eat(VAR)
        decs = []
        while self.current_token.type == ID:
            decs.extend(self.declaration())
            self.eat(SEMI)
        return decs
    def compound(self):
        """compound: BEGIN statement_list END"""
        self.eat(BEGIN)
        nodes = self.statement_list()
        self.eat(END)
        return nodes
    def statement(self):
        """statement: assignment_statement | compound_statement |empty"""


    def statement_list(self):
        """statement_list: statement | SEMI statement_list"""
        statement_list = [self.statement()]
        while self.current_token.type == SEMI:
            self.eat(SEMI)
            statement_list.append(self.statement())
    def block(self):
        """block: declarations compound"""
        declarations = self.declarations()
        compound = self.compound()
        return Block(declarations,compound)

    def program(self):
        """program: PROGRAM variable SEMI BLOCK DOT"""
        self.eat(PROGRAM)
        name = self.variable()
        self.eat(SEMI)
        block = self.block()
