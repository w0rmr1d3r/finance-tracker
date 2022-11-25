import csv

from deprecated.classic import deprecated

from finance_tracker.entries.entry import Entry
from finance_tracker.money.currency_codes import CurrencyCodes
from finance_tracker.money.money import Money
from finance_tracker.readers.base_reader import BaseReader


@deprecated(reason="Use the internal one in EntryReader", version="1.0.0")
def float_in_str_to_str(to_convert: str) -> float:
    return float(to_convert.replace(".", "").replace(",", "."))


class EntryReader(BaseReader):
    """
    Default reader of entries.
    """

    _HEADERS_TO_IGNORE = 3

    def read_from_file(self, path_to_file: str) -> list:
        """
        Reads entries from the given file

        :param path_to_file: Path to file with entries
        :return: List of Entry
        """
        return self.read_entries_from_file(headers_to_ignore=self._HEADERS_TO_IGNORE, path_to_file=path_to_file)

    @staticmethod
    def float_in_str_to_str(to_convert: str) -> float:
        """
        Converts float numbers in strings with the format of "1.000,00" to float numbers in Python

        :param to_convert: float number within a string
        :return: float converted
        """
        return float(to_convert.replace(".", "").replace(",", "."))

    @deprecated(reason="Use <read_from_file> instead from this class.", version="1.3.0")
    def read_entries_from_file(self, headers_to_ignore: int, path_to_file: str) -> list[Entry]:
        """
        DEPRECATED - Use read_from_file instead.

        Reads entries from a given file. Will ignore a given amount of headers.

        :param headers_to_ignore: Headers to ignore from file
        :param path_to_file: Path to file with entries
        :return: list of Entry objects
        """
        entries = []
        with open(path_to_file, "r", encoding="UTF-8") as file:
            csvreader = csv.reader(file, dialect="excel", delimiter=";")
            for _ in range(headers_to_ignore):
                next(csvreader)

            for row in csvreader:
                entries.append(
                    Entry(
                        entry_date=row[0],
                        date_of_action=row[1],
                        title=row[2],
                        other_data=row[3],
                        quantity=Money(amount=self.float_in_str_to_str(row[4]), currency_code=CurrencyCodes.EUR),
                        balance=Money(amount=self.float_in_str_to_str(row[5]), currency_code=CurrencyCodes.EUR),
                    )
                )
        return entries
