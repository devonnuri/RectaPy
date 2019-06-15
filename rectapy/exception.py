class SyntaxError(Exception):
    pass


class ParseError(Exception):
    pass


class RuntimeError(Exception):
    pass


class ReturnTrigger(RuntimeError):
    def __init__(self, value):
        self.value = value
