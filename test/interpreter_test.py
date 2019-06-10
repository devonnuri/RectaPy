from rectapy import Lexer, Parser, Interpreter

if __name__ == '__main__':
    lexer = Lexer("""
var a = "global a";
var b = "global b";
var c = "global c";
{
  var a = "outer a";
  var b = "outer b";
  {
    var a = "inner a";
  }
}
""".strip())

    tokens = lexer.lex()

    parser = Parser(tokens)

    statements = parser.parse()

    interpreter = Interpreter()

    interpreter.interpret(statements)
