from typing import List

from rectapy import Token


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens

    def parse(self):
        statements = []

    def expression(self):
        pass

    def declaration(self):
        pass

    def statement(self):
        pass

    def _for(self):
        pass

    def _if(self):
        pass

    def _return(self):
        pass

    def _var(self):
        pass

    def _while(self):
        pass

    def function(self):
        pass

    def block(self):
        pass

    def assignment(self):
        pass

    def _or(self):
        pass

    def _and(self):
        pass

    def equality(self):
        pass

    def comparison(self):
        pass

    def addition(self):
        pass

    def multiplication(self):
        pass

    def unary(self):
        pass

    def finish_call(self):
        pass

    def call(self):
        pass

    def primary(self):
        pass

    def match(self):
        pass

    def consume(self):
        pass

    def check(self):
        pass

    def advance(self):
        pass

    def is_end(self):
        pass

    def peek(self):
        pass

    def previous(self):
        pass

    def synchronize(self):
        pass
