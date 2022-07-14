from typing import Any

import rectapy


class RectaPy:
    def __init__(self):
        self.interpreter = rectapy.Interpreter()
        self.resolver = rectapy.Resolver(self.interpreter)

    def run(self, code: str):
        lexer = rectapy.Lexer(code)
        tokens = lexer.lex()

        parser = rectapy.Parser(tokens)
        statements = parser.parse()

        self.resolver.resolve(statements)

        return self.interpreter.interpret(statements)

    def run_file(self, filename: str) -> None:
        with open(filename, 'r') as f:
            self.run(f.read())

    def run_prompt(self) -> None:
        try:
            while True:
                print('> ', end='')
                result = self.run(input())
                if result:
                    print(result)
        except KeyboardInterrupt:
            pass
