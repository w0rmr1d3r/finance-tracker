import pathlib

import pytest

from finance_tracker.readers.trading212_reader import Trading212Reader


@pytest.fixture
def reader() -> Trading212Reader:
    return Trading212Reader()


def test_trading212_reader_reads_a_card_debit_entry(reader):
    current_path = pathlib.Path(__file__).parent.resolve()
    path_to_file = f"{current_path}/files/test_trading212_reader_one_card_debit_entry.csv"
    result = reader.read_from_file(path_to_file=path_to_file)

    assert len(result) == 1
    assert result[0].action == "Card debit"
    assert result[0].time == "2024-03-15 10:30:00"
    assert result[0].total == -25.50
    assert result[0].currency_total == "EUR"
    assert result[0].merchant_name == "Coffee Shop"


def test_trading212_reader_reads_entry_without_merchant(reader):
    current_path = pathlib.Path(__file__).parent.resolve()
    path_to_file = f"{current_path}/files/test_trading212_reader_one_entry_no_merchant.csv"
    result = reader.read_from_file(path_to_file=path_to_file)

    assert len(result) == 1
    assert result[0].action == "Market buy"
    assert result[0].total == 100.00
    assert result[0].currency_total == "EUR"
    assert not result[0].merchant_name


def test_trading212_reader_normalizes_dividend_action(reader):
    current_path = pathlib.Path(__file__).parent.resolve()
    path_to_file = f"{current_path}/files/test_trading212_reader_dividend_entry.csv"
    result = reader.read_from_file(path_to_file=path_to_file)

    assert len(result) == 1
    assert result[0].action == "Dividend"
    assert result[0].total == 1.50
    assert result[0].currency_total == "USD"


def test_trading212_reader_skips_rows_without_total(reader):
    current_path = pathlib.Path(__file__).parent.resolve()
    path_to_file = f"{current_path}/files/test_trading212_reader_skips_empty_total.csv"
    result = reader.read_from_file(path_to_file=path_to_file)

    assert len(result) == 0


def test_trading212_reader_reads_several_entries(reader):
    current_path = pathlib.Path(__file__).parent.resolve()
    path_to_file = f"{current_path}/files/test_trading212_reader_several_entries.csv"
    result = reader.read_from_file(path_to_file=path_to_file)

    assert len(result) == 10


def test_trading212_reader_does_nothing_on_empty_file(reader):
    current_path = pathlib.Path(__file__).parent.resolve()
    path_to_file = f"{current_path}/files/test_trading212_reader_no_entries.csv"
    result = reader.read_from_file(path_to_file=path_to_file)

    assert len(result) == 0
