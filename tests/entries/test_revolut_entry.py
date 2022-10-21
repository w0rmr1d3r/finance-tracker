from datetime import date

from finance_tracker.money.currency_codes import CurrencyCodes
from finance_tracker.money.money import Money


def test_revolut_entry_can_be_built(revolut_entry):
    assert revolut_entry.type == "CARD_PAYMENT"
    assert revolut_entry.product == "Current"
    assert revolut_entry.started_date == "2022-10-02 15:01:02"
    assert revolut_entry.completed_date == "2022-10-03 15:01:02"
    assert revolut_entry.description == "Supermarket purchase"
    assert revolut_entry.amount == -4
    assert revolut_entry.fee == 0
    assert revolut_entry.currency == "EUR"
    assert revolut_entry.state == "COMPLETED"
    assert revolut_entry.balance == 100


def test_revolut_entry_quantity_is_money(revolut_entry):
    assert revolut_entry.quantity() == Money(amount=-4, currency_code=CurrencyCodes.EUR)


def test_revolut_entry_dates_as_time(revolut_entry):
    assert revolut_entry.started_date == "2022-10-02 15:01:02"
    assert revolut_entry.completed_date == "2022-10-03 15:01:02"
    # we don't care about smaller time units
    assert revolut_entry.started_date_as_time() == date(day=2, month=10, year=2022)
    assert revolut_entry.started_date_as_time() == date(day=2, month=10, year=2022)
    assert revolut_entry.month_from_started_date() == 10
    assert revolut_entry.month_from_completed_date_of_action() == 10


def test_revolut_entry_balance_as_money(revolut_entry):
    assert revolut_entry.balance_as_money() == Money(amount=100, currency_code=CurrencyCodes.EUR)


def test_revolut_entry_quantity_as_absolut(revolut_entry):
    assert revolut_entry.quantity_as_absolute() == Money(amount=4, currency_code=CurrencyCodes.EUR)


def test_revolut_entry_dates_for_entry(revolut_entry):
    assert revolut_entry.started_date == "2022-10-02 15:01:02"
    assert revolut_entry.completed_date == "2022-10-03 15:01:02"
    # we don't care about smaller time units
    assert revolut_entry.started_date_for_entry() == "2/10/2022"
    assert revolut_entry.completed_date_for_entry() == "3/10/2022"
