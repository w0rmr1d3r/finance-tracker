import csv

from finance_tracker.entries.santander_entry import SantanderEntry
from finance_tracker.readers.base_reader import BaseReader


class SantanderReader(BaseReader):
    """
    Reader for Santander files
    """

    _HEADERS_TO_IGNORE = 1

    def read_from_file(self, path_to_file: str) -> list:
        """
        Reads entries from the given file and returns a list of SantanderEntry

        :param path_to_file: Path to file with Santander entries
        :return: list of SantanderEntry
        """
        entries = []
        with open(path_to_file, "r", encoding="UTF-8") as file:
            csvreader = csv.reader(file, delimiter=";")
            for _ in range(self._HEADERS_TO_IGNORE):
                next(csvreader)

            for row in csvreader:
                entries.append(
                    SantanderEntry(
                        operation_date=row[0],
                        value_date=row[1],
                        concept=row[2],
                        amount=self._parse_amount(row[3]),
                        balance=self._parse_amount(row[4]),
                    )
                )

        return entries

    @staticmethod
    def _parse_amount(value: str) -> float:
        return float(value.replace(".", "").replace(",", "."))
