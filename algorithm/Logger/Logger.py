NO_PRINT = True
NO_WRITE = True


class Logger:
    @staticmethod
    def print(string):
        if not NO_PRINT:
            print(string)

    @staticmethod
    def write(write: lambda: int):
        if not NO_WRITE:
            write()
