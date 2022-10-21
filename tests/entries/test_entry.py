from datetime import date

from finance_tracker.entries.entry import Entry
from finance_tracker.money.currency_codes import CurrencyCodes
from finance_tracker.money.money import Money


def test_entry_can_be_built(entry):
    assert entry.entry_date == "01/02/2022"
    assert entry.date_of_action == "03/05/2022"
    assert entry.title == "ACTION"
    assert entry.other_data == "test"
    assert entry.quantity == Money(amount=1.56, currency_code="EUR")
    assert entry.balance == Money(amount=-1.56, currency_code="EUR")


def test_entry_dates_as_time(entry):
    assert entry.entry_date == "01/02/2022"
    assert entry.date_of_action == "03/05/2022"
    assert entry.date_as_time() == date(day=1, month=2, year=2022)
    assert entry.month_from_date() == 2
    assert entry.date_of_action_as_time() == date(day=3, month=5, year=2022)
    assert entry.month_from_date_of_action() == 5


def test_entry_from_revolut_entry(revolut_entry):
    entry = Entry.from_revolut_entry(revolut_entry)
    assert entry.entry_date == "2/10/2022"
    assert entry.date_as_time() == date(day=2, month=10, year=2022)
    assert entry.date_of_action == "3/10/2022"
    assert entry.date_of_action_as_time() == date(day=3, month=10, year=2022)
    assert entry.title == "Supermarket purchase"
    assert entry.other_data == ""
    assert entry.quantity == Money(amount=4, currency_code=CurrencyCodes.EUR)
    assert entry.balance == Money(amount=100, currency_code=CurrencyCodes.EUR)
