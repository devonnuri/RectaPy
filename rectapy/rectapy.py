class RectaPy:
    @staticmethod
    def run(code: str) -> None:
        pass

    @staticmethod
    def run_file(filename: str) -> None:
        with open(filename, 'r') as f:
            RectaPy.run(f.read())

    @staticmethod
    def run_prompt() -> None:
        try:
            while True:
                print('> ', end='')
                RectaPy.run(input())
        except KeyboardInterrupt:
            pass
