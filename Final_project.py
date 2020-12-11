#!/usr/bin/env python
# coding: utf-8

# In[4]:


INTEGER, PLUS, MINUS, MUL, DIV, EOF = (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', 'EOF'
)

#token class
class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, MINUS, MUL, DIV, or EOF
        self.type = type
        # token value: non-negative integer value, '+', '-', '*', '/', or None
        self.value = value

    def __str__(self):
        #String depiction.
        #Examples include Token(INTEGER, 2), Token(PLUS, '+'), TOKEN(MINUS '-')
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

#Lexer class
class Lexer(object):
    def __init__(self, string_input):
        # User string_input like 2*2, 2/2, 2-2 etc.
        self.string_input = string_input
        # self.pos is an index into self.text. initial values will be the 0th index position
        self.pos = 0
        self.current_char = self.string_input[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        #Advance the `pos` pointer and set the `current_char` variable
        self.pos += 1
        if self.pos > len(self.string_input) - 1: #finding the length 
            self.current_char = None  # Indicates end of input which means there is no other character after this
        else:
            self.current_char = self.string_input[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        #Return the integer from the provided input. 
        Return_value = ''
        while self.current_char is not None and self.current_char.isdigit():
            Return_value += self.current_char
            self.advance()
        return int(Return_value)#returns integer output

    def get_next_token(self):
        # tokenizer where the input data is divided into individual tokens to identify the type, value etc. 
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

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            self.error()

        return Token(EOF, None)


class Interpreter(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # Assign the current token to the first token
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        # comparison of the current token with the token that is passed and if they are identical then eat the current token
        # and assign the next token to the self.current_token, otherwise raise an exception(exception handling)
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
       #Integer factor
        token = self.current_token
        self.eat(INTEGER)
        return token.value

    def term(self):
       # term multiplication and division factor 
        Return_value = self.factor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
                Return_value = Return_value * self.factor()
            elif token.type == DIV:
                self.eat(DIV)
                Return_value = Return_value / self.factor()

        return Return_value

    def expr(self):
       
        Return_value = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                Return_value = Return_value + self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                Return_value = Return_value - self.term()

        return Return_value


def main():
    while True:
        try:
            string_input = input('Enter the numbers and the arithmetic operation for the calculator> ')
        except EOFError:
            break
        if not string_input:
            continue
        lexer = Lexer(string_input)
        interpreter = Interpreter(lexer)
        Return_value = interpreter.expr()
        print(Return_value)


if __name__ == '__main__':
    main()


# In[ ]:




