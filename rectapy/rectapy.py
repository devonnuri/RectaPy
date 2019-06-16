from typing import Any

import rectapy


class RectaPy:
    def __init__(self):
        self.interpreter = rectapy.Interpreter()

    def run(self, code: str) -> Any:
        lexer = rectapy.Lexer(code)
        tokens = lexer.lex()

        parser = rectapy.Parser(tokens)
        statements = parser.parse()

        return self.interpreter.interpret(statements)

    def run_file(self, filename: str) -> None:
        with open(filename, 'r') as f:
            self.run(f.read())

    def run_prompt(self) -> None:
        try:
            while True:
                print('> ', end='')
                print(self.run(input()))
        except KeyboardInterrupt:
            pass
