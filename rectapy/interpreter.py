from typing import List

from rectapy import TokenType, Environment, RectaRuntimeError, expression as expr, statement as stmt, Callable, Function, \
    ReturnTrigger


class Interpreter(expr.ExprVisitor, stmt.StmtVisitor):
    def __init__(self):
        self.globals = Environment()
        self.environment = self.globals

    def interpret(self, statements: List[stmt.Statement]):
        last_value = None
        try:
            for statement in statements:
                last_value = self.execute(statement)
        except RectaRuntimeError as error:
            print(error)

        return stringify(last_value)

    def evaluate(self, expression: expr.Expression):
        return expression.accept(self) if expression else None

    def execute(self, statement: stmt.Statement):
        return statement.accept(self) if statement else None

    def execute_block(self, statements: List[stmt.Statement], environment: Environment):
        previous = self.environment

        try:
            self.environment = environment

            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    def visit_assign(self, expression: expr.Assign):
        value = self.evaluate(expression.value)

        self.environment.assign(expression.value, value)
        return value

    def visit_binary(self, expression: expr.Binary):
        left = self.evaluate(expression.left)
        right = self.evaluate(expression.right)
        opertype = expression.operator.type

        if opertype == TokenType.PLUS and (check(float, left, right) or check(str, left, right)):
            return left + right
        elif opertype == TokenType.MINUS and check(float, left, right):
            return left - right
        elif opertype == TokenType.STAR and check(float, left, right):
            return left * right
        elif opertype == TokenType.SLASH and check(float, left, right):
            return left / right
        elif opertype == TokenType.GREATER and check(float, left, right):
            return left > right
        elif opertype == TokenType.GREATER_EQUAL and check(float, left, right):
            return left >= right
        elif opertype == TokenType.LESS and check(float, left, right):
            return left < right
        elif opertype == TokenType.LESS_EQUAL and check(float, left, right):
            return left <= right
        elif opertype == TokenType.EQUAL_EQUAL:
            return left == right
        elif opertype == TokenType.EXCLAM_EQUAL:
            return left != right

        return None

    def visit_call(self, expression: expr.Call):
        callee = self.evaluate(expression.callee)
        arguments = list(map(self.evaluate, expression.arguments))

        if not isinstance(callee, Callable):
            raise RectaRuntimeError('Only functions are callable.')

        if len(arguments) != callee.arity():
            raise RectaRuntimeError(f'Expected {callee.arity()} arguments but got {len(arguments)}.')

        return callee.call(self, arguments)

    def visit_get(self, expression: expr.Get):
        pass

    def visit_grouping(self, expression: expr.Grouping):
        return self.evaluate(expression)

    def visit_literal(self, expression: expr.Literal):
        return expression.value

    def visit_logical(self, expression: expr.Logical):
        left = self.evaluate(expression.left)

        if expression.operator.type == TokenType.OR:
            if is_truthy(left):
                return left
        elif not is_truthy(left):
            return left

        return self.evaluate(expression.right)

    def visit_set(self, expression: expr.Set):
        pass

    def visit_unary(self, expression: expr.Unary):
        right = self.evaluate(expression.operand)
        opertype = expression.operator.type

        if opertype == TokenType.EXCLAM:
            return not is_truthy(right)
        elif opertype == TokenType.MINUS:
            if isinstance(right, float):
                return -right
            else:
                raise RectaRuntimeError('Bad operand type for unary -')

        return None

    def visit_variable_get(self, expression: expr.Variable):
        return self.environment.get(expression.name)

    def visit_block(self, statement: stmt.Block):
        self.execute_block(statement.statements, Environment(self.environment))

    def visit_expression(self, statement: stmt.Expression):
        return self.evaluate(statement.expression)

    def visit_function(self, statement: stmt.Function):
        function = Function(statement, self.environment)
        self.environment.define(statement.name.lexeme, function)

    def visit_if(self, statement: stmt.If):
        if is_truthy(self.evaluate(statement.condition)):
            self.execute(statement.then_branch)
        elif statement.else_branch is not None:
            self.execute(statement.else_branch)

    def visit_return(self, statement: stmt.Return):
        value = None if statement.value is None else self.evaluate(statement.value)

        raise ReturnTrigger(value)

    def visit_variable_set(self, statement: stmt.Var):
        value = None
        if statement.initializer is not None:
            value = self.evaluate(statement.initializer)

        self.environment.define(statement.name.lexeme, value)

    def visit_while(self, statement: stmt.While):
        while is_truthy(self.evaluate(statement.condition)):
            self.execute(statement.body)

    def visit_for(self, statement: stmt.For):
        # TODO: Implement for statement
        pass


def is_truthy(value: object) -> bool:
    if value is None:
        return False

    if isinstance(value, bool):
        return value

    if isinstance(value, float):
        return value != 0

    return True


def stringify(value: object) -> str:
    if value is None:
        return 'null'

    if isinstance(value, float):
        return '%g' % value

    return str(value)


def check(value_type: type, *values: object) -> bool:
    return all(isinstance(value, value_type) for value in values)
