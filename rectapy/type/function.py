from rectapy import Environment, statement as stmt, ReturnTrigger

from .callable import Callable


class Function(Callable):
    def __init__(self, function: stmt.Function):
        self.function = function

    def arity(self) -> int:
        return len(self.function.parameters)

    def call(self, interpreter, arguments):
        environment = Environment(interpreter.globals)
        for parameter, argument in zip(self.function.parameters, arguments):
            environment.define(parameter.lexeme, argument)

        try:
            interpreter.execute_block(self.function.body, environment)
        except ReturnTrigger as trigger:
            return trigger.value

        return None
