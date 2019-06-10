from rectapy import Lexer

if __name__ == '__main__':
    lexer = Lexer("""
// asdf
for i in range(10) {
    i.string().print()
}
    """.strip())

    tokens = lexer.lex()

    print('\n'.join(map(str, tokens)))
