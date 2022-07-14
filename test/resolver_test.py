from rectapy import Lexer, Parser, Interpreter, Resolver

if __name__ == '__main__':
    lexer = Lexer("""
var a = "outer";
{
    var b = "inner";
    
    fun fbib(a) {
        print a;
    }
    print b;
}
print a;
""".strip())

    tokens = lexer.lex()

    parser = Parser(tokens)

    statements = parser.parse()

    interpreter = Interpreter()

    resolver = Resolver(interpreter)
    resolver.resolve(statements)

    interpreter.interpret(statements)
