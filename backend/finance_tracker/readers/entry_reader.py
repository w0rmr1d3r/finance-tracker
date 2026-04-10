import csv

from finance_tracker.constants import ENCODING
from finance_tracker.entries.entry import Entry
from finance_tracker.money.currency_codes import CurrencyCodes
from finance_tracker.money.money import DEFAULT_MONEY, Money
from finance_tracker.readers.base_reader import BaseReader


class EntryReader(BaseReader):
    """
    Default reader of entries.
    """

    _HEADERS_TO_IGNORE = 1

    def read_from_file(self, path_to_file: str) -> list:
        """
        Reads entries from the given file.
        Supports both semicolon-delimited and comma-delimited formats,
        detected automatically from the header.

        :param path_to_file: Path to file with entries
        :return: List of Entry
        """
        entries = []
        with open(path_to_file, "r", encoding=ENCODING) as file:
            first_line = file.readline()
            file.seek(0)

            delimiter = ";" if ";" in first_line else ","

            csvreader = csv.reader(file, dialect="excel", delimiter=delimiter)
            for _ in range(self._HEADERS_TO_IGNORE):
                next(csvreader)

            for row in csvreader:
                entries.append(
                    Entry(
                        entry_date=row[0],
                        date_of_action=row[0],
                        title=row[1],
                        other_data=row[2],
                        quantity=Money(amount=self.float_in_str_to_str(row[3]), currency_code=CurrencyCodes.EUR),
                        balance=DEFAULT_MONEY,
                    )
                )
        return entries

    @staticmethod
    def float_in_str_to_str(to_convert: str) -> float:
        """
        Converts float numbers in strings with the format of "1000,00" to float numbers in Python

        :param to_convert: float number within a string
        :return: float converted
        """
        return float(to_convert.replace(",", "."))
