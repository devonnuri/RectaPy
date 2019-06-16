import sys

from rectapy import RectaPy


def main() -> None:
    rectapy = RectaPy()
    if len(sys.argv) == 1:
        rectapy.run_prompt()
    elif len(sys.argv) == 2:
        rectapy.run_file(sys.argv[1])
    else:
        print('Usage: rectapy [filename]')
        exit(64)


if __name__ == '__main__':
    main()
