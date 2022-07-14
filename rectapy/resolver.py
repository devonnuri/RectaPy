from typing import List, Dict

from rectapy import expression as expr, statement as stmt, Token, TokenType, RectaRuntimeError
from rectapy.interpreter import Interpreter


class Resolver(expr.ExprVisitor, stmt.StmtVisitor):
    def __init__(self, interpreter: Interpreter):
        self.interpreter = interpreter
        self.scopes: List[Dict[str, bool]] = []

    def resolve(self, statements: List[stmt.Statement]):
        for statement in statements:
            self.resolve_statement(statement)

    def resolve_statement(self, statement: stmt.Statement):
        statement.accept(self)

    def resolve_expression(self, expression: expr.Expression):
        expression.accept(self)

    def resolve_local(self, expression: expr.Expression, name: Token):
        for i, scope in enumerate(reversed(self.scopes)):
            if name.lexeme in scope:
                self.interpreter.resolve(expression, i)
                return

    def resolve_function(self, function: stmt.Function):
        self.begin_scope()
        for parameter in function.parameters:
            self.declare(parameter)
            self.define(parameter)
        self.resolve(function.body)
        self.end_scope()

    def begin_scope(self):
        self.scopes.append({})

    def end_scope(self):
        self.scopes.pop()

    def declare(self, name: Token):
        if not self.scopes:
            return

        scope = self.scopes[-1]

        if name.lexeme in scope:
            raise RectaRuntimeError('Variable with this name already declared in this scope.')

        scope[name.lexeme] = False

    def define(self, name: Token):
        if not self.scopes:
            return

        self.scopes[-1][name.lexeme] = True

    def visit_block(self, statement: stmt.Block):
        self.begin_scope()
        self.resolve(statement.statements)
        self.end_scope()

    def visit_variable_get(self, expression: expr.Variable):
        if self.scopes and not self.scopes[-1][expression.name.lexeme]:
            raise RectaRuntimeError('Cannot read local variable in its own initializer')

        self.resolve_local(expression, expression.name)

    def visit_variable_set(self, statement: stmt.Var):
        self.declare(statement.name)

        if statement.initializer:
            self.resolve_expression(statement.initializer)

        self.define(statement.name)

    def visit_assign(self, expression: expr.Assign):
        self.resolve_expression(expression.value)
        self.resolve_local(expression, expression.name)

    def visit_function(self, statement: stmt.Function):
        self.declare(statement.name)
        self.define(statement.name)

        self.resolve_function(statement)

    def visit_expression(self, statement: stmt.Expression):
        self.resolve_expression(statement.expression)

    def visit_if(self, statement: stmt.If):
        self.resolve_expression(statement.condition)
        self.resolve_statement(statement.then_branch)

        if statement.else_branch:
            self.resolve_statement(statement.else_branch)

    def visit_print(self, statement: stmt.Print):
        self.resolve_expression(statement.expression)

    def visit_return(self, statement: stmt.Return):
        if statement.value:
            self.resolve_expression(statement.value)

    def visit_for(self, statement: stmt.For):
        pass

    def visit_while(self, statement: stmt.While):
        self.resolve_expression(statement.condition)
        self.resolve_statement(statement.body)

    def visit_binary(self, expression: expr.Binary):
        self.resolve_expression(expression.left)
        self.resolve_expression(expression.right)

    def visit_call(self, expression: expr.Call):
        self.resolve_expression(expression.callee)

        for argument in expression.arguments:
            self.resolve_expression(argument)

    def visit_get(self, expression: expr.Get):
        pass

    def visit_set(self, expression: expr.Set):
        pass

    def visit_grouping(self, expression: expr.Grouping):
        self.resolve_expression(expression.expression)

    def visit_literal(self, expression: expr.Literal):
        pass

    def visit_logical(self, expression: expr.Logical):
        self.resolve_expression(expression.left)
        self.resolve_expression(expression.right)

    def visit_unary(self, expression: expr.Unary):
        self.resolve_expression(expression.operand)

