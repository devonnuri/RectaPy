from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List

from .expression import Expression as Expr
from rectapy import Token

R = TypeVar('R')


class StmtVisitor(ABC, Generic[R]):

    @abstractmethod
    def visit_block(self, stmt: Block) -> R:
        pass

    @abstractmethod
    def visit_expression(self, stmt: Expression) -> R:
        pass

    @abstractmethod
    def visit_function(self, stmt: Function) -> R:
        pass

    @abstractmethod
    def visit_if(self, stmt: If) -> R:
        pass

    @abstractmethod
    def visit_return(self, expr: Return) -> R:
        pass

    @abstractmethod
    def visit_var(self, expr: Var) -> R:
        pass

    @abstractmethod
    def visit_while(self, expr: While) -> R:
        pass

    @abstractmethod
    def visit_for(self, expr: For) -> R:
        pass


class Statement(ABC, Generic[R]):
    @abstractmethod
    def accept(self, visitor: StmtVisitor) -> R:
        pass


class Block(Statement, Generic[R]):
    def __init__(self, statements: List[Statement]):
        self.statements = statements

    def accept(self, visitor: StmtVisitor[R]) -> R:
        return visitor.visit_block(self)


class Expression(Statement, Generic[R]):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: StmtVisitor[R]) -> R:
        return visitor.visit_expression(self)


class Function(Statement, Generic[R]):
    def __init__(self, name: Token, parameters: List[Token], body: List[Statement]):
        self.name = name
        self.parameters = parameters
        self.body = body

    def accept(self, visitor: StmtVisitor[R]) -> R:
        return visitor.visit_function(self)


class If(Statement, Generic[R]):
    def __init__(self, condition: Expr, then_branch: Statement, else_branch: Statement):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor: StmtVisitor[R]) -> R:
        return visitor.visit_if(self)


class Return(Statement, Generic[R]):
    def __init__(self, keyword: Token, value: Expr):
        self.keyword = keyword
        self.value = value

    def accept(self, visitor: StmtVisitor[R]) -> R:
        return visitor.visit_return(self)


class Var(Statement, Generic[R]):
    def __init__(self, name: Token, initializer: Expr):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor: StmtVisitor[R]) -> R:
        return visitor.visit_var(self)


class While(Statement, Generic[R]):
    def __init__(self, condition: Expr, body: Statement):
        self.condition = condition
        self.body = body

    def accept(self, visitor: StmtVisitor[R]) -> R:
        return visitor.visit_while(self)


class For(Statement, Generic[R]):
    def __init__(self, element: Token, iterable: Expr, body: Statement):
        self.element = element
        self.iterable = iterable
        self.body = body

    def accept(self, visitor: StmtVisitor[R]) -> R:
        return visitor.visit_for(self)
