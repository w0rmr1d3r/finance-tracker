import pathlib

import pytest

from finance_tracker.readers.trade_republic_reader import TradeRepublicReader


@pytest.fixture
def reader() -> TradeRepublicReader:
    return TradeRepublicReader()


def test_trade_republic_reader_reads_a_buy_entry(reader):
    current_path = pathlib.Path(__file__).parent.resolve()
    path_to_file = f"{current_path}/files/test_trade_republic_reader_one_buy_entry.csv"
    result = reader.read_from_file(path_to_file=path_to_file)

    assert len(result) == 1
    assert result[0].type == "BUY"
    assert result[0].datetime == "2026-08-03T07:48:42.436Z"
    assert result[0].amount == -50.00
    assert result[0].fee == -1.00
    assert result[0].tax == 0.0
    assert result[0].currency == "EUR"


def test_trade_republic_reader_reads_a_sell_entry(reader):
    current_path = pathlib.Path(__file__).parent.resolve()
    path_to_file = f"{current_path}/files/test_trade_republic_reader_one_sell_entry.csv"
    result = reader.read_from_file(path_to_file=path_to_file)

    assert len(result) == 1
    assert result[0].type == "SELL"
    assert result[0].amount == 53.74
    assert result[0].fee == -1.00
    assert result[0].tax == 0.0
    assert result[0].currency == "EUR"


def test_trade_republic_reader_reads_a_dividend_entry_with_tax(reader):
    current_path = pathlib.Path(__file__).parent.resolve()
    path_to_file = f"{current_path}/files/test_trade_republic_reader_dividend_with_tax.csv"
    result = reader.read_from_file(path_to_file=path_to_file)

    assert len(result) == 1
    assert result[0].type == "DIVIDEND"
    assert result[0].amount == 0.04
    assert result[0].fee == 0.0
    assert result[0].tax == -0.02
    assert result[0].currency == "EUR"


def test_trade_republic_reader_uses_zero_for_empty_fee_and_tax(reader):
    current_path = pathlib.Path(__file__).parent.resolve()
    path_to_file = f"{current_path}/files/test_trade_republic_reader_cash_transfer_no_fee_or_tax.csv"
    result = reader.read_from_file(path_to_file=path_to_file)

    assert len(result) == 1
    assert result[0].type == "TRANSFER_INSTANT_INBOUND"
    assert result[0].amount == 100.0
    assert result[0].fee == 0.0
    assert result[0].tax == 0.0
    assert result[0].currency == "EUR"


@pytest.mark.parametrize(
    "filename,expected_count",
    [
        ("test_trade_republic_reader_several_entries.csv", 11),
        ("test_trade_republic_reader_no_entries.csv", 0),
    ],
)
def test_trade_republic_reader_result_count(reader, filename, expected_count):
    current_path = pathlib.Path(__file__).parent.resolve()
    path_to_file = f"{current_path}/files/{filename}"
    result = reader.read_from_file(path_to_file=path_to_file)

    assert len(result) == expected_count


def test_trade_republic_reader_skips_empty_rows_mid_file(reader):
    current_path = pathlib.Path(__file__).parent.resolve()
    path_to_file = f"{current_path}/files/test_trade_republic_reader_empty_row_mid_file.csv"
    result = reader.read_from_file(path_to_file=path_to_file)

    assert len(result) == 2
    assert result[0].type == "BUY"
    assert result[1].type == "SELL"


@pytest.mark.parametrize(
    "headers,name,expected",
    [
        (["type", "datetime", "amount"], "type", 0),
        (["type", "datetime", "amount"], "amount", 2),
        (["type", "datetime", "amount"], "missing", None),
        (["  type  ", " datetime ", " amount "], "amount", 2),
        ([], "type", None),
    ],
)
def test_find_column_index_by_name(headers, name, expected):
    assert TradeRepublicReader._find_column_index_by_name(headers, name) == expected
