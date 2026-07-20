import csv
import logging

from finance_tracker.constants import ENCODING
from finance_tracker.entries.trading212_entry import Trading212Entry
from finance_tracker.readers.base_reader import BaseReader

logger = logging.getLogger(__name__)


class Trading212Reader(BaseReader):
    """
    Reader for Trading212 full-export CSV files.
    """

    _MERCHANT_COL_NAME = "Merchant name"
    _TOTAL_COL_NAME = "Total"
    _ACTION_COL_NAME = "Action"
    _TIME_COL_NAME = ("Time", "Time (UTC)")
    _CURRENCY_TOTAL_COL_NAMES = ("Currency (Total)", "Currency(Total)")

    @staticmethod
    def _find_column_index_by_possible_names(headers: list, *names: str) -> int | None:
        stripped = [h.strip() for h in headers]
        for name in names:
            try:
                return stripped.index(name)
            except ValueError:
                continue
        return None

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

            # Find the index of the columns that are needed
            action_col = self._find_column_index_by_possible_names(headers, self._ACTION_COL_NAME)
            time_col = self._find_column_index_by_possible_names(headers, *self._TIME_COL_NAME)
            total_col = self._find_column_index_by_possible_names(headers, self._TOTAL_COL_NAME)
            currency_col = self._find_column_index_by_possible_names(headers, *self._CURRENCY_TOTAL_COL_NAMES)
            merchant_col = self._find_column_index_by_possible_names(headers, self._MERCHANT_COL_NAME)

            for row in csvreader:
                # If we find an empty row or a new line, we skip it.
                if not row:
                    logger.warning("Empty row found, skipping.")
                    continue

                # In some cases, there are rows without a "total"
                # for which we assign 0.0 as the new assigned value and warn about it
                total_str = row[total_col]
                if not total_str:
                    logger.warning(
                        "There's an entry with no total in %s, assigning 0.0 as new total",
                        path_to_file,
                    )
                    total_str = "0.0"

                action = row[action_col]
                # Override action value for any dividend
                if action.startswith("Dividend"):
                    action = "Dividend"

                total = float(total_str)
                if action == "Market buy":
                    total = -abs(total)

                entries.append(
                    Trading212Entry(
                        action=action,
                        time=row[time_col],
                        total=total,
                        currency_total=row[currency_col],
                        merchant_name=row[merchant_col] if merchant_col is not None and len(row) > merchant_col else "",
                    )
                )

        return entries
