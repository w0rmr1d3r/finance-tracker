class BaseReader:
    _HEADERS_TO_IGNORE: int = 0

    def read_from_file(self, path_to_file: str) -> list:
        pass
