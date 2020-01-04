from rectapy import Lexer, Parser, Interpreter

if __name__ == '__main__':
    lexer = Lexer("""
fun fibonacci(n) {
   if n <= 1 {
     return n;
   }
   return fibonacci(n - 2) + fibonacci(n - 1);
}

fibonacci(10);
""".strip())

    tokens = lexer.lex()

    parser = Parser(tokens)

    statements = parser.parse()

    interpreter = Interpreter()

    print(interpreter.interpret(statements))
