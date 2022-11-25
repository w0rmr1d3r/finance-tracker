import pathlib

import pytest

from finance_tracker.money.money import Money
from finance_tracker.readers.entry_reader import EntryReader


@pytest.fixture
def reader() -> EntryReader:
    return EntryReader()


def test_entry_reader_reads_an_entry(reader):
    current_path = pathlib.Path(__file__).parent.resolve()
    path_to_file = f"{current_path}/files/test_entry_reader_one_entry.csv"
    result = reader.read_from_file(path_to_file=path_to_file)

    assert len(result) == 1
    assert result[0].balance == Money(currency_code="EUR", amount=1000)
    assert result[0].date_of_action == "01/01/1999"
    assert result[0].entry_date == "01/01/1999"
    assert result[0].other_data == "PAYCHECK FROM COMPANY 1"
    assert result[0].quantity == Money(currency_code="EUR", amount=1000)
    assert result[0].title == "PAYCHECK"


def test_entry_reader_reads_several_entries(reader):
    current_path = pathlib.Path(__file__).parent.resolve()
    path_to_file = f"{current_path}/files/test_entry_reader_several_entries.csv"
    result = reader.read_from_file(path_to_file=path_to_file)

    assert len(result) == 10


def test_entry_reader_does_nothing_on_empty_file(reader):
    current_path = pathlib.Path(__file__).parent.resolve()
    path_to_file = f"{current_path}/files/test_entry_reader_no_entries.csv"
    result = reader.read_from_file(path_to_file=path_to_file)

    assert len(result) == 0


def test_float_in_str_to_str_returns_correct_value():
    assert 1000.0 == EntryReader.float_in_str_to_str("1.000")
