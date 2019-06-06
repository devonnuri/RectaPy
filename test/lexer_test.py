from rectapy import RectaPy

if __name__ == '__main__':
    RectaPy.run("""
// asdf
if a <= 2 {
    'something'.print()
}
""".strip())
