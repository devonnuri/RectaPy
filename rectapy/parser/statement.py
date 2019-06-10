from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar, List

from .expression import Expression as Expr
from rectapy import Token

R = TypeVar('R')


class StmtVisitor(ABC):

    @abstractmethod
    def visit_block(self, statement: Block):
        pass

    @abstractmethod
    def visit_expression(self, statement: Expression):
        pass

    @abstractmethod
    def visit_function(self, statement: Function):
        pass

    @abstractmethod
    def visit_if(self, statement: If):
        pass

    @abstractmethod
    def visit_return(self, expression: Return):
        pass

    @abstractmethod
    def visit_variable_set(self, expression: Var):
        pass

    @abstractmethod
    def visit_while(self, expression: While):
        pass

    @abstractmethod
    def visit_for(self, expression: For):
        pass


class Statement(ABC):
    @abstractmethod
    def accept(self, visitor: StmtVisitor):
        pass


class Block(Statement):
    def __init__(self, statements: List[Statement]):
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_block(self)


class Expression(Statement):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_expression(self)


class Function(Statement):
    def __init__(self, name: Token, parameters: List[Token], body: List[Statement]):
        self.name = name
        self.parameters = parameters
        self.body = body

    def accept(self, visitor):
        return visitor.visit_function(self)


class If(Statement):
    def __init__(self, condition: Expr, then_branch: Statement, else_branch: Statement):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor):
        return visitor.visit_if(self)


class Return(Statement):
    def __init__(self, keyword: Token, value: Expr):
        self.keyword = keyword
        self.value = value

    def accept(self, visitor):
        return visitor.visit_return(self)


class Var(Statement):
    def __init__(self, name: Token, initializer: Expr):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor):
        return visitor.visit_variable_set(self)


class While(Statement):
    def __init__(self, condition: Expr, body: Statement):
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        return visitor.visit_while(self)


class For(Statement):
    def __init__(self, element: Token, iterable: Expr, body: Statement):
        self.element = element
        self.iterable = iterable
        self.body = body

    def accept(self, visitor):
        return visitor.visit_for(self)
