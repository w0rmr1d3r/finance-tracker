from datetime import date

from finance_tracker.entries.trading212_entry import Trading212Entry
from finance_tracker.money.currency_codes import CurrencyCodes
from finance_tracker.money.money import Money


def test_trading212_entry_can_be_built(trading212_entry):
    assert trading212_entry.action == "Card debit"
    assert trading212_entry.time == "2024-03-15 10:30:00"
    assert trading212_entry.total == -25.50
    assert trading212_entry.currency_total == "EUR"
    assert trading212_entry.merchant_name == "Coffee Shop"


def test_trading212_entry_quantity_is_money(trading212_entry):
    assert trading212_entry.quantity() == Money(amount=-25.50, currency_code=CurrencyCodes.EUR)


def test_trading212_entry_quantity_uses_currency_total():
    entry = Trading212Entry(
        action="Dividend",
        time="2024-01-15 09:00:00",
        total=1.50,
        currency_total="USD",
        merchant_name="",
    )
    assert entry.quantity() == Money(amount=1.50, currency_code=CurrencyCodes.USD)


def test_trading212_entry_time_as_date(trading212_entry):
    assert trading212_entry.time_as_date() == date(day=15, month=3, year=2024)


def test_trading212_entry_time_for_entry(trading212_entry):
    assert trading212_entry.time_for_entry() == "15/03/2024"
