from finance_tracker.readers.entry_reader import EntryReader
from finance_tracker.readers.reader_dispatcher import detect_reader
from finance_tracker.readers.revolut_reader import RevolutReader
from finance_tracker.readers.santander_reader import SantanderReader
from finance_tracker.readers.trading212_reader import Trading212Reader


def test_detect_revolut_header():
    header = "Type,Product,Started Date,Completed Date,Description,Amount,Fee,Currency,State,Balance"
    assert isinstance(detect_reader(header), RevolutReader)


def test_detect_santander_header_comma():
    header = "FECHA OPERACIÓN,FECHA VALOR,CONCEPTO,IMPORTE EUR,SALDO"
    assert isinstance(detect_reader(header), SantanderReader)


def test_detect_santander_header_semicolon():
    header = "FECHA OPERACIÓN;FECHA VALOR;CONCEPTO;IMPORTE EUR;SALDO"
    assert isinstance(detect_reader(header), SantanderReader)


def test_detect_trading212_header():
    header = (
        "Action,Time,ISIN,Ticker,Name,Notes,ID,No. of shares,Price / share,Currency (Price / share),"
        "Exchange rate,Result,Currency (Result),Total,Currency (Total),Withholding tax,"
        "Currency (Withholding tax),Merchant name,Merchant category,French transaction tax,"
        "Currency (French transaction tax)"
    )
    assert isinstance(detect_reader(header), Trading212Reader)


def test_detect_default_header_comma():
    header = "DATE,TITLE,DESCRIPTION,QUANTITY"
    assert isinstance(detect_reader(header), EntryReader)


def test_detect_default_header_semicolon():
    header = "DATE;TITLE;DESCRIPTION;QUANTITY"
    assert isinstance(detect_reader(header), EntryReader)


def test_detect_unknown_returns_none():
    header = "foo,bar,baz"
    assert detect_reader(header) is None
