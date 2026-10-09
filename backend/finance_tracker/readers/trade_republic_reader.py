import csv
import logging

from finance_tracker.constants import ENCODING
from finance_tracker.entries.trade_republic_entry import TradeRepublicEntry
from finance_tracker.readers.base_reader import BaseReader

logger = logging.getLogger(__name__)


class TradeRepublicReader(BaseReader):
    """
    Reader for TradeRepublic full-export CSV files.
    """

    _TYPE_COL_NAME = "type"
    _DATETIME_COL_NAME = "datetime"
    _AMOUNT_COL_NAME = "amount"
    _FEE_COL_NAME = "fee"
    _TAX_COL_NAME = "tax"
    _CURRENCY_COL_NAME = "currency"

    @staticmethod
    def _find_column_index_by_name(headers: list, name: str) -> int | None:
        stripped = [h.strip() for h in headers]
        try:
            return stripped.index(name)
        except ValueError:
            return None

    @staticmethod
    def _parse_float(value: str) -> float:
        return float(value) if value else 0.0

    def read_from_file(self, path_to_file: str) -> list:
        """
        Reads entries from the given TradeRepublic CSV file and returns a list of TradeRepublicEntry.

        :param path_to_file: Path to the TradeRepublic CSV export file
        :return: list of TradeRepublicEntry
        """
        entries = []
        with open(path_to_file, "r", encoding=ENCODING) as file:
            csvreader = csv.reader(file, delimiter=",")
            headers = next(csvreader)

            # Find the index of the columns that are needed
            type_col = self._find_column_index_by_name(headers, self._TYPE_COL_NAME)
            datetime_col = self._find_column_index_by_name(headers, self._DATETIME_COL_NAME)
            amount_col = self._find_column_index_by_name(headers, self._AMOUNT_COL_NAME)
            fee_col = self._find_column_index_by_name(headers, self._FEE_COL_NAME)
            tax_col = self._find_column_index_by_name(headers, self._TAX_COL_NAME)
            currency_col = self._find_column_index_by_name(headers, self._CURRENCY_COL_NAME)

            for row in csvreader:
                # If we find an empty row or a new line, we skip it.
                if not row:
                    logger.warning("Empty row found, skipping.")
                    continue

                entries.append(
                    TradeRepublicEntry(
                        type=row[type_col],
                        datetime=row[datetime_col],
                        amount=self._parse_float(row[amount_col]),
                        fee=self._parse_float(row[fee_col]),
                        tax=self._parse_float(row[tax_col]),
                        currency=row[currency_col],
                    )
                )

        return entries
