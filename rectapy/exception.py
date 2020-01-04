class RectaSyntaxError(BaseException):
    pass


class RectaParseError(BaseException):
    pass


class RectaRuntimeError(BaseException):
    pass


class ReturnTrigger(RectaRuntimeError):
    def __init__(self, value):
        self.value = value
