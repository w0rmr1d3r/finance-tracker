from datetime import date

from finance_tracker.money.currency_codes import CurrencyCodes
from finance_tracker.money.money import Money


def test_trade_republic_entry_can_be_built(trade_republic_entry):
    assert trade_republic_entry.type == "BUY"
    assert trade_republic_entry.datetime == "2026-08-03T07:48:42.436Z"
    assert trade_republic_entry.amount == -50.00
    assert trade_republic_entry.fee == -1.00
    assert trade_republic_entry.tax == 0.0
    assert trade_republic_entry.currency == "EUR"


def test_trade_republic_entry_quantity_combines_amount_fee_and_tax(trade_republic_entry):
    assert trade_republic_entry.quantity() == Money(amount=-51.00, currency_code=CurrencyCodes.EUR)


def test_trade_republic_entry_quantity_uses_currency(trade_republic_entry_dividend):
    assert trade_republic_entry_dividend.quantity() == Money(amount=0.02, currency_code=CurrencyCodes.EUR)


def test_trade_republic_entry_datetime_as_date(trade_republic_entry):
    assert trade_republic_entry._datetime_as_date() == date(day=3, month=8, year=2026)


def test_trade_republic_entry_datetime_for_entry(trade_republic_entry):
    assert trade_republic_entry.datetime_for_entry() == "03/08/2026"
