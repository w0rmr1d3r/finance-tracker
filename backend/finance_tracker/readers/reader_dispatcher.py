import logging

from finance_tracker.constants import ENCODING
from finance_tracker.entries.entry import Entry
from finance_tracker.readers.entry_reader import EntryReader
from finance_tracker.readers.revolut_reader import RevolutReader
from finance_tracker.readers.santander_reader import SantanderReader
from finance_tracker.readers.trading212_reader import Trading212Reader

logger = logging.getLogger(__name__)


def _read_header_line(path_to_file: str) -> str:
    with open(path_to_file, "r", encoding=ENCODING) as file:
        first_line = file.readline()
    return first_line.lstrip("﻿").strip()


def detect_reader(header_line: str):
    """
    Inspect the CSV header line and return the matching reader instance, or None
    if the format is not recognised.

    :param header_line: First line of a CSV file (BOM stripped)
    :return: A reader instance with read_from_file(), or None
    """
    if "Started Date" in header_line and "Completed Date" in header_line:
        return RevolutReader()
    if "FECHA OPERACIÓN" in header_line and "CONCEPTO" in header_line:
        return SantanderReader()
    if "Action" in header_line and "Currency (Total)" in header_line:
        return Trading212Reader()
    if "DATE" in header_line and "TITLE" in header_line:
        return EntryReader()
    return None


def _convert(reader, raw_entries):
    if isinstance(reader, RevolutReader):
        return [Entry.from_revolut_entry(e) for e in raw_entries]
    if isinstance(reader, SantanderReader):
        return [Entry.from_santander_entry(e) for e in raw_entries]
    if isinstance(reader, Trading212Reader):
        return [Entry.from_trading212_entry(e) for e in raw_entries]
    return list(raw_entries)


def read_into_entries(path_to_file: str, entries: list) -> bool:
    """
    Detect bank format from header and append generic Entry objects to entries.

    :param path_to_file: Path to a CSV file
    :param entries: List to extend with Entry objects
    :return: True if a matching reader was found, False otherwise
    """
    header = _read_header_line(path_to_file)
    reader = detect_reader(header)
    if reader is None:
        logger.warning("Unknown CSV format for %s, skipping", path_to_file)
        return False
    raw = reader.read_from_file(path_to_file)
    entries.extend(_convert(reader, raw))
    return True
