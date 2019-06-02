import sys

from rectapy import RectaPy


def main() -> None:
    if len(sys.argv) == 1:
        RectaPy.run_prompt()
    elif len(sys.argv) == 2:
        RectaPy.run_file(sys.argv[1])
    else:
        print('Usage: rectapy [filename]')
        exit(64)


if __name__ == '__main__':
    main()
