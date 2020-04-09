INTEGER, PLUS, MINUS, EOF = 'INTEGER', 'PLUS', 'MINUS', 'EOF'


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type},{value})'.format(type=self.type, value=self.value)

    def __repr__(self):
        return self.__str__()


class Interpreter(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid syntax')

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def integer(self):
        r = ''
        while self.pos < len(self.text) and self.text[self.pos].isdigit():
            r += self.current_char
            self.advance()
        return int(r)

    def get_next_token(self):
        text = self.text
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())
            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')
            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')
            self.error()
        return Token(EOF, None)

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def eat(self, type):
        if self.current_token.type == type:
            current_token = self.current_token
            self.current_token = self.get_next_token()
            return current_token.value
        else:
            self.error()

    def expr(self):
        r = 0
        self.current_token = self.get_next_token()
        r = self.eat(INTEGER)
        while self.current_token.type != EOF:
            if self.current_token.type == PLUS:
                self.eat(PLUS)
                r += self.eat(INTEGER)
            if self.current_token.type == MINUS:
                self.eat(MINUS)
                r -= self.eat(INTEGER)
        return r


def main():
    text = ' 12 + 4 -  2 '
    interpreter = Interpreter(text)
    print(interpreter.expr())


if __name__ == '__main__':
    main()
