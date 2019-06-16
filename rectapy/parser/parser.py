from typing import List, Optional

from . import expression as expr
from . import statement as stmt
from rectapy import Token, ParseError, TokenType


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> List[stmt.Statement]:
        statements = []
        while not self.is_end():
            statements.append(self.declaration())

        return statements

    def expression(self) -> expr.Expression:
        return self.assignment()

    def declaration(self) -> Optional[stmt.Statement]:
        try:
            if self.match(TokenType.VAR):
                return self.var()

            if self.match(TokenType.FUN):
                return self.function()

            return self.statement()
        except ParseError as error:
            print(error)

            self.synchronize()

            return None

    def statement(self) -> stmt.Statement:
        if self.match(TokenType.FOR):
            return self._for()

        if self.match(TokenType.IF):
            return self._if()

        if self.match(TokenType.RETURN):
            return self._return()

        if self.match(TokenType.WHILE):
            return self._while()

        if self.match(TokenType.LEFT_BRACE):
            return stmt.Block(self.block())

        return self.expressionStatement()

    def expressionStatement(self) -> stmt.Statement:
        expression = self.expression()
        self.consume(TokenType.SEMICOLON, 'Expect \';\' after expression.')
        return stmt.Expression(expression)

    def _for(self) -> stmt.Statement:
        element = self.consume(TokenType.IDENTIFIER, 'Expect element after \'for\'.')
        self.consume(TokenType.IN, 'Expect \'in\' after element.')
        iterable = self.expression()
        body = self.statement()

        return stmt.For(element, iterable, body)

    def _if(self) -> stmt.Statement:
        condition = self.expression()
        then_branch = self.statement()
        else_branch = self.statement() if self.match(TokenType.ELSE) else None

        return stmt.If(condition, then_branch, else_branch)

    def _return(self) -> stmt.Statement:
        keyword = self.peek(-1)
        value = None if self.match(TokenType.SEMICOLON) else self.expression()

        self.consume(TokenType.SEMICOLON, 'Expect \';\' after return value.')

        return stmt.Return(keyword, value)

    def var(self) -> stmt.Statement:
        name = self.consume(TokenType.IDENTIFIER, 'Expect variable name.')
        initializer = self.expression() if self.match(TokenType.EQUAL) else None
        self.consume(TokenType.SEMICOLON, 'Expect \';\' after variable declaration.')

        return stmt.Var(name, initializer)

    def _while(self) -> stmt.Statement:
        condition = self.expression()
        body = self.statement()

        return stmt.While(condition, body)

    def function(self) -> stmt.Statement:
        name = self.consume(TokenType.IDENTIFIER, 'Expect function name')
        self.consume(TokenType.LEFT_PAREN, 'Expect \'(\' after function name.')

        parameters = []
        if not self.check(TokenType.RIGHT_PAREN):
            parameters.append(self.consume(TokenType.IDENTIFIER, 'Expect parameter name.'))
            while self.match(TokenType.COMMA):
                parameters.append(self.consume(TokenType.IDENTIFIER, 'Expect parameter name.'))
        self.consume(TokenType.RIGHT_PAREN, 'Expect \')\' after parameters.')

        if self.match(TokenType.LEFT_BRACE):
            body = self.block()
        else:
            body = [self.statement()]

        return stmt.Function(name, parameters, body)

    def block(self) -> List[stmt.Statement]:
        statements = []

        while not self.check(TokenType.RIGHT_BRACE) and not self.is_end():
            statements.append(self.declaration())

        self.consume(TokenType.RIGHT_BRACE, 'Expect \'}\' after block.')

        return statements

    def assignment(self) -> expr.Expression:
        expression = self._or()

        if self.match(TokenType.EQUAL):
            value = self.assignment()

            if isinstance(expression, expr.Variable):
                expression.__class__ = expr.Variable
                return expr.Assign(expression.name, value)
            elif isinstance(expression, expr.Get):
                expression.__class__ = expr.Get

                return expr.Set(expression.target, expression.name, value)

            raise ParseError('Invalid assignment target.')

        return expression

    def _or(self) -> expr.Expression:
        expression = self._and()

        while self.match(TokenType.OR):
            operator = self.peek(-1)
            right = self._and()
            expression = expr.Logical(expression, operator, right)

        return expression

    def _and(self) -> expr.Expression:
        expression = self.equality()

        while self.match(TokenType.AND):
            operator = self.peek(-1)
            right = self.equality()
            expression = expr.Logical(expression, operator, right)

        return expression

    def equality(self) -> expr.Expression:
        expression = self.comparison()

        while self.match(TokenType.EXCLAM_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.peek(-1)
            right = self.comparison()
            expression = expr.Binary(expression, operator, right)

        return expression

    def comparison(self) -> expr.Expression:
        expression = self.addition()

        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.peek(-1)
            right = self.addition()
            expression = expr.Binary(expression, operator, right)

        return expression

    def addition(self) -> expr.Expression:
        expression = self.multiplication()

        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.peek(-1)
            right = self.multiplication()
            expression = expr.Binary(expression, operator, right)

        return expression

    def multiplication(self) -> expr.Expression:
        expression = self.unary()

        while self.match(TokenType.STAR, TokenType.SLASH):
            operator = self.peek(-1)
            right = self.unary()
            expression = expr.Binary(expression, operator, right)

        return expression

    def unary(self) -> expr.Expression:
        if self.match(TokenType.EXCLAM, TokenType.MINUS):
            operator = self.peek(-1)
            right = self.unary()
            return expr.Unary(operator, right)

        return self.pre_call()

    def pre_call(self) -> expr.Expression:
        expression = self.primary()

        while True:
            if self.match(TokenType.LEFT_PAREN):
                expression = self.post_call(expression)
            elif self.match(TokenType.DOT):
                name = self.consume(TokenType.IDENTIFIER, 'Expect property name after \'.\'')
                expression = expr.Get(expression, name)
            else:
                break

        return expression

    def post_call(self, callee: expr.Expression) -> expr.Expression:
        arguments = []
        if not self.check(TokenType.RIGHT_PAREN):
            arguments.append(self.expression())
            while self.match(TokenType.COMMA):
                arguments.append(self.expression())

        parenthesis = self.consume(TokenType.RIGHT_PAREN, 'Expect \')\' after parameters.')

        return expr.Call(callee, parenthesis, arguments)

    def primary(self) -> expr.Expression:
        if self.match(TokenType.FALSE):
            return expr.Literal(False)

        if self.match(TokenType.TRUE):
            return expr.Literal(True)

        if self.match(TokenType.NULL):
            return expr.Literal(None)

        if self.match(TokenType.NUMBER, TokenType.SINGLE_STRING, TokenType.DOUBLE_STRING):
            return expr.Literal(self.peek(-1).literal)

        if self.match(TokenType.IDENTIFIER):
            return expr.Variable(self.peek(-1))

        if self.match(TokenType.LEFT_PAREN):
            expression = self.expression()
            self.consume(TokenType.RIGHT_PAREN, 'Expect \')\' after expression.')
            return expr.Grouping(expression)

        raise ParseError(self.peek(), 'Expect expression.')

    def match(self, *types: TokenType) -> bool:
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True

        return False

    def consume(self, token_type: TokenType, message: str) -> Token:
        if self.check(token_type):
            return self.advance()

        raise ParseError(message)

    def check(self, token_type: TokenType) -> bool:
        if self.is_end():
            return False
        return self.peek().type == token_type

    def advance(self) -> Token:
        if not self.is_end():
            self.current += 1

        return self.peek(-1)

    def is_end(self) -> bool:
        return self.peek().type == TokenType.EOF

    def peek(self, offset: Optional[int] = 0):
        return self.tokens[self.current + offset] if 0 <= self.current + offset < len(self.tokens) else None

    def synchronize(self) -> None:
        self.advance()

        while not self.is_end():
            if self.peek(-1).type == TokenType.SEMICOLON:
                return

            if self.peek().type in [TokenType.IF, TokenType.FUN, TokenType.VAR, TokenType.FOR, TokenType.WHILE,
                                    TokenType.RETURN]:
                return

            self.advance()
