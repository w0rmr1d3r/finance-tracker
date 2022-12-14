import csv

from finance_tracker.entries.revolut_entry import RevolutEntry
from finance_tracker.readers.base_reader import BaseReader


class RevolutReader(BaseReader):
    """
    Reader for Revolut files
    """

    _HEADERS_TO_IGNORE = 1

    def read_from_file(self, path_to_file: str) -> list:
        """
        Reads entries from the given file and returns a list of RevolutEntry

        :param path_to_file: Path to file with revolut entries
        :return: list of RevolutEntry
        """
        entries = []
        with open(path_to_file, "r", encoding="ASCII") as file:
            csvreader = csv.reader(file, dialect="excel", delimiter=",")
            for _ in range(self._HEADERS_TO_IGNORE):
                next(csvreader)

            for row in csvreader:
                entries.append(
                    RevolutEntry(
                        type=row[0],
                        product=row[1],
                        started_date=row[2],
                        completed_date=row[3],
                        description=row[4],
                        amount=float(row[5]),
                        fee=float(row[6]),
                        currency=row[7],
                        state=row[8],
                        balance=float(row[9]),
                    )
                )

        return entries
