import csv

from finance_tracker.constants import ENCODING
from finance_tracker.entries.trading212_entry import Trading212Entry
from finance_tracker.readers.base_reader import BaseReader


class Trading212Reader(BaseReader):
    """
    Reader for Trading212 full-export CSV files.
    """

    _MERCHANT_COL_NAME = "Merchant name"

    def read_from_file(self, path_to_file: str) -> list:
        """
        Reads entries from the given Trading212 CSV file and returns a list of Trading212Entry.

        :param path_to_file: Path to the Trading212 CSV export file
        :return: list of Trading212Entry
        """
        entries = []
        with open(path_to_file, "r", encoding=ENCODING) as file:
            csvreader = csv.reader(file, delimiter=",")
            headers = next(csvreader)
            merchant_col = next(
                (i for i, h in enumerate(headers) if h.strip() == self._MERCHANT_COL_NAME),
                None,
            )

            for row in csvreader:
                if not row:
                    continue
                total_str = row[13]
                if not total_str:
                    continue

                action = row[0]
                if action.startswith("Dividend"):
                    action = "Dividend"

                entries.append(
                    Trading212Entry(
                        action=action,
                        time=row[1],
                        total=float(total_str),
                        currency_total=row[14],
                        merchant_name=row[merchant_col] if merchant_col is not None and len(row) > merchant_col else "",
                    )
                )

        return entries
