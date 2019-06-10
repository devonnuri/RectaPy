from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from rectapy import Token


class ExprVisitor(ABC):

    @abstractmethod
    def visit_assign(self, expression: Assign):
        pass

    @abstractmethod
    def visit_binary(self, expression: Binary):
        pass

    @abstractmethod
    def visit_call(self, expression: Call):
        pass

    @abstractmethod
    def visit_get(self, expression: Get):
        pass

    @abstractmethod
    def visit_grouping(self, expression: Grouping):
        pass

    @abstractmethod
    def visit_literal(self, expression: Literal):
        pass

    @abstractmethod
    def visit_logical(self, expression: Logical):
        pass

    @abstractmethod
    def visit_set(self, expression: Set):
        pass

    @abstractmethod
    def visit_unary(self, expression: Unary):
        pass

    @abstractmethod
    def visit_variable_get(self, expression: Variable):
        pass


class Expression(ABC):
    @abstractmethod
    def accept(self, visitor: ExprVisitor):
        pass


class Assign(Expression):
    def __init__(self, name: Token, value: Expression):
        self.name = name
        self.value = value

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_assign(self)


class Binary(Expression):
    def __init__(self, left: Expression, operator: Token, right: Expression):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_binary(self)


class Call(Expression):
    def __init__(self, callee: Expression, parenthesis: Token, arguments: List[Expression]):
        self.callee = callee
        self.parenthesis = parenthesis
        self.arguments = arguments

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_call(self)


class Get(Expression):
    def __init__(self, target: Expression, name: Token):
        self.target = target
        self.name = name

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_get(self)


class Grouping(Expression):
    def __init__(self, expression: Expression):
        self.expression = expression

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_grouping(self)


class Literal(Expression):
    def __init__(self, value: object):
        self.value = value

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_literal(self)


class Logical(Expression):
    def __init__(self, left: Expression, operator: Token, right: Expression):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_logical(self)


class Set(Expression):
    def __init__(self, target: Expression, name: Token, value: Expression):
        self.target = target
        self.name = name
        self.value = value

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_set(self)


class Unary(Expression):
    def __init__(self, operator: Token, operand: Expression):
        self.operator = operator
        self.operand = operand

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_unary(self)


class Variable(Expression):
    def __init__(self, name: Token):
        self.name = name

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_variable_get(self)
