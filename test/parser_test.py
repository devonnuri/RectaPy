from rectapy import Lexer, Parser

if __name__ == '__main__':
    lexer = Lexer("""
// asdf
for i in range(10) {
    i.string().print()
}
""".strip())

    tokens = lexer.lex()
    print('Lex finished')

    parser = Parser(tokens)

    statements = parser.parse()

