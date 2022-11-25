from abc import ABC, abstractmethod


class BaseReader(ABC):
    _HEADERS_TO_IGNORE: int = 0

    @abstractmethod
    def read_from_file(self, path_to_file: str) -> list:
        """
        Base method, please implement a strategy instead.

        Reads entries from given file and returns list of entries.

        :param path_to_file: Path to the file to read entries from
        :return: Returns list of entries read.
        """
        pass
