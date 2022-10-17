import csv

from finance_tracker.entries.entry import Entry
from finance_tracker.money.currency_codes import CurrencyCodes
from finance_tracker.money.money import Money
from finance_tracker.readers.base_reader import BaseReader


def float_in_str_to_str(to_convert: str) -> float:
    return float(to_convert.replace(".", "").replace(",", "."))

# todo - in progress + test
class RevolutReader(BaseReader):
    _HEADERS_TO_IGNORE = 1

    def read_from_file(self, path_to_file: str) -> list:
        entries = []
        with open(path_to_file, "r") as file:
            csvreader = csv.reader(file, dialect="excel", delimiter=";")
            for _ in range(self._HEADERS_TO_IGNORE):
                next(csvreader)

            for row in csvreader:
                entries.append(
                    Entry(
                        entry_date=row[0],
                        date_of_action=row[1],
                        title=row[2],
                        other_data=row[3],
                        quantity=Money(amount=float_in_str_to_str(row[4]), currency_code=CurrencyCodes.EUR),
                        balance=Money(amount=float_in_str_to_str(row[5]), currency_code=CurrencyCodes.EUR),
                    )
                )
        return entries
