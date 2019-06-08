from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List

from rectapy import Token

R = TypeVar('R')


class ExprVisitor(ABC, Generic[R]):

    @abstractmethod
    def visit_assign(self, expr: Assign) -> R:
        pass

    @abstractmethod
    def visit_binary(self, expr: Binary) -> R:
        pass

    @abstractmethod
    def visit_call(self, expr: Call) -> R:
        pass

    @abstractmethod
    def visit_get(self, expr: Get) -> R:
        pass

    @abstractmethod
    def visit_grouping(self, expr: Grouping) -> R:
        pass

    @abstractmethod
    def visit_literal(self, expr: Literal) -> R:
        pass

    @abstractmethod
    def visit_logical(self, expr: Logical) -> R:
        pass

    @abstractmethod
    def visit_set(self, expr: Set) -> R:
        pass

    @abstractmethod
    def visit_unary(self, expr: Unary) -> R:
        pass

    @abstractmethod
    def visit_variable(self, expr: Variable) -> R:
        pass


class Expression(ABC, Generic[R]):
    @abstractmethod
    def accept(self, visitor: ExprVisitor) -> R:
        pass


class Assign(Expression, Generic[R]):
    def __init__(self, name: Token, value: Expression):
        self.name = name
        self.value = value

    def accept(self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_assign(self)


class Binary(Expression, Generic[R]):
    def __init__(self, left: Expression, operator: Token, right: Expression):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_binary(self)


class Call(Expression, Generic[R]):
    def __init__(self, callee: Expression, parenthesis: Token, arguments: List[Expression]):
        self.callee = callee
        self.parenthesis = parenthesis
        self.arguments = arguments

    def accept(self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_call(self)


class Get(Expression, Generic[R]):
    def __init__(self, target: Expression, name: Token):
        self.target = target
        self.name = name

    def accept(self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_get(self)


class Grouping(Expression, Generic[R]):
    def __init__(self, expression: Expression):
        self.expression = expression

    def accept(self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_grouping(self)


class Literal(Expression, Generic[R]):
    def __init__(self, value: object):
        self.value = value

    def accept(self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_literal(self)


class Logical(Expression, Generic[R]):
    def __init__(self, left: Expression, operator: Token, right: Expression):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_logical(self)


class Set(Expression, Generic[R]):
    def __init__(self, target: Expression, name: Token, value: Expression):
        self.target = target
        self.name = name
        self.value = value

    def accept(self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_set(self)


class Unary(Expression, Generic[R]):
    def __init__(self, operator: Token, right: Expression):
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_unary(self)


class Variable(Expression, Generic[R]):
    def __init__(self, name: Token):
        self.name = name

    def accept(self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_variable(self)
