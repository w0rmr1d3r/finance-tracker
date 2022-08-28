class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    @classmethod
    def print_header(cls, message: str) -> None:
        print(f"{bcolors.HEADER}{message}{bcolors.ENDC}")

    @classmethod
    def print_blue(cls, message: str) -> None:
        print(f"{bcolors.OKBLUE}{message}{bcolors.ENDC}")

    @classmethod
    def print_cyan(cls, message: str) -> None:
        print(f"{bcolors.OKCYAN}{message}{bcolors.ENDC}")

    @classmethod
    def print_green(cls, message: str) -> None:
        print(f"{bcolors.OKGREEN}{message}{bcolors.ENDC}")

    @classmethod
    def print_warning(cls, message: str) -> None:
        print(f"{bcolors.WARNING}{message}{bcolors.ENDC}")

    @classmethod
    def print_fail(cls, message: str) -> None:
        print(f"{bcolors.FAIL}{message}{bcolors.ENDC}")

    @classmethod
    def print_bold(cls, message: str) -> None:
        print(f"{bcolors.BOLD}{message}{bcolors.ENDC}")

    @classmethod
    def print_underline(cls, message: str) -> None:
        print(f"{bcolors.UNDERLINE}{message}{bcolors.ENDC}")
