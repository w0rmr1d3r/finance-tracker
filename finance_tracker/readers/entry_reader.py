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
    _HEADERS_TO_IGNORE = 3

    def read_from_file(self, path_to_file: str) -> list:
        return self.read_entries_from_file(headers_to_ignore=self._HEADERS_TO_IGNORE, path_to_file=path_to_file)

    @staticmethod
    def float_in_str_to_str(to_convert: str) -> float:
        return float(to_convert.replace(".", "").replace(",", "."))

    # todo - test
    def read_entries_from_file(self, headers_to_ignore: int, path_to_file: str) -> list[Entry]:
        entries = []
        with open(path_to_file, "r") as file:
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
