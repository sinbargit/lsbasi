(PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, ID, ASSIGN, BEGIN, END, INTEGER, SEMI, DOT, EOF) = (
    'PLUS', 'MINUS', 'MUL', 'DIV', 'LPAREN', 'RPAREN', 'ID', 'ASSIGN', 'BEGIN', 'END', 'INTEGER', 'SEMI', 'DOT', 'EOF')


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(type=self.type, value=self.value)

    def __repr__(self):
        return self.__str__()


RESERVED_KEYWORDS = {
    'BEGIN': Token('BEGIN', 'BEGIN'),
    'END': Token('END', 'END')
}


class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        r = ''
        while self.current_char is not None and self.current_char.isdigit():
            r += self.current_char
            self.advance()
        return int(r)

    def _id(self):
        r = ''
        while self.current_char is not None and self.current_char.isalnum():
            r += self.current_char
            self.advance()
        return RESERVED_KEYWORDS.get(r, Token(ID, r))

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace:
                self.skip_whitespace()
            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())
            if self.current_char.isalnum():
                return self._id()
            if self.current_char == '(':
                return Token(LPAREN, '(')
            if self.current_char == ')':
                return Token(RPAREN, ')')
            if self.current_char == '.':
                return Token(DOT, '.')
            if self.current_char == '+':
                return Token(PLUS, '+')
            if self.current_char == '-':
                return Token(MINUS, '-')
            if self.current_char == '*':
                return Token(MUL, '*')
            if self.current_char == '/':
                return Token(DIV, '/')
            if self.current_char == ':' and self.peek() == '=':
                return Token(ASSIGN, ':=')
            if self.current_char == ';':
                return Token(SEMI, ';')
            else:
                return self.error()
        return Token(EOF, None)


class AST(object):
    pass


class BinOp(AST):
    def __init__(self, left, op, right):
        self.token = self.op = op
        self.left = left
        self.right = right


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr


class Compound(AST):
    def __init__(self):
        self.children = []


class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class NoOp(AST):
    pass


class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token == self.lexer.get_next_token()

    def error(self):
        raise Exception('syntax error')

    def eat(self, type):
        if self.current_token.type == type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def program(self):
        node = self.compound_statement()
        self.eat(DOT)
        return node

    def compound_statement(self):
        self.eat(BEGIN)
        nodes = self.statement_list()
        self.eat(END)
        root = Compound()
        root.children = nodes
        return root

    def statement_list(self):
        node = self.statement()
        nodes = [node]
        while self.current_token == SEMI:
            nodes.append(self.statement())
        return nodes

    def statement(self):
        if self.current_token.type == BEGIN:
            return self.compound_statement()
        if self.current_token.type == ID:
            return self.assignment_statement()
        else:
            return self.empty()

    def assignment_statement(self):
        left = self.variable()
        token = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        return Assign(left, token, right)

    def empty(self):
        return NoOp

    def variable(self):
        node = Var(self.current_token)
        self.eat(ID)
        return node

    def expr(self):
        node = self.term()
        while self.current_token.type == MINUS or self.current_token.type == PLUS:
            token = self.current_token
            self.eat(self.current_token.type)
            node = BinOp(node, token, self.term())
        return node

    def term(self):
        node = self.factor()
        while self.current_token.type == MUL or self.current_token.type == DIV:
            token = self.current_token
            self.eat(self.current_token.type)
            node = BinOp(node, token, self.factor())
        return node

    def factor(self):
        token = self.current_token
        if token.type == MUL or token.type == DIV:
            return UnaryOp(token, self.factor())
        if token.type == INTEGER:
            return Num(token)
        if token.type == ID:
            return self.variable()
        else:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node

    def parse(self):
        node = self.program()
        if self.current_token.type != EOF:
            self.error()
        else:
            return node


class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class Interpreter(NodeVisitor):
    GLOBAL_SCOPE = {}

    def __init__(self, parser):
        self.parser = parser

    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        if node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        if node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        if node.op.type == DIV:
            return self.visit(node.left) / self.visit(node.right)

    def visit_Num(self, node):
        return node.value

    def visit_UnaryOp(self, node):
        return self.visit(node)

    def visit_Assign(self, node):
        self.GLOBAL_SCOPE[node.left.value] = self.visit(node.right)

    def visit_Var(self, node):
        var = self.GLOBAL_SCOPE.get(node.value)
        if var is None:
            raise NameError(repr(var))
        else:
            return var

    def visit_NoOp(self, node):
        return None

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def interpret(self):
        tree = self.parser.parse()
        self.visit(tree)


def main():
    import sys
    text = open(sys.argv[1], 'r').read()
    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.interpret()
    print(interpreter.GLOBAL_SCOPE)


if __name__ == '__main__':
    main()
