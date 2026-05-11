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


def test_trading212_reader_uses_zero_for_empty_total(reader):
    current_path = pathlib.Path(__file__).parent.resolve()
    path_to_file = f"{current_path}/files/test_trading212_reader_uses_zero_for_empty_total.csv"
    result = reader.read_from_file(path_to_file=path_to_file)

    assert len(result) == 1
    assert result[0].total == 0.0


@pytest.mark.parametrize(
    "filename,expected_count",
    [
        ("test_trading212_reader_several_entries.csv", 10),
        ("test_trading212_reader_no_entries.csv", 0),
    ],
)
def test_trading212_reader_result_count(reader, filename, expected_count):
    current_path = pathlib.Path(__file__).parent.resolve()
    path_to_file = f"{current_path}/files/{filename}"
    result = reader.read_from_file(path_to_file=path_to_file)

    assert len(result) == expected_count


def test_trading212_reader_finds_merchant_when_at_col_17(reader):
    current_path = pathlib.Path(__file__).parent.resolve()
    path_to_file = f"{current_path}/files/test_trading212_reader_merchant_at_col_17.csv"
    result = reader.read_from_file(path_to_file=path_to_file)

    assert len(result) == 1
    assert result[0].action == "Card debit"
    assert result[0].total == -25.50
    assert result[0].currency_total == "EUR"
    assert result[0].merchant_name == "Coffee Shop"


def test_trading212_reader_finds_merchant_when_at_col_19(reader):
    current_path = pathlib.Path(__file__).parent.resolve()
    path_to_file = f"{current_path}/files/test_trading212_reader_merchant_at_col_19.csv"
    result = reader.read_from_file(path_to_file=path_to_file)

    assert len(result) == 1
    assert result[0].action == "Card debit"
    assert result[0].total == -25.50
    assert result[0].currency_total == "EUR"
    assert result[0].merchant_name == "Coffee Shop"
