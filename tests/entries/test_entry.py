from datetime import date

from finance_tracker.entries.entry import Entry
from finance_tracker.money.money import Money


def test_entry_can_be_built():
    entry = Entry(
        entry_date="01/01/2022",
        date_of_action="01/01/2022",
        title="ACTION",
        other_data="test",
        quantity=Money(amount=1.56, currency_code="EUR"),
        balance=Money(amount=-1.56, currency_code="EUR"),
    )
    assert entry.entry_date == "01/01/2022"
    assert entry.date_of_action == "01/01/2022"
    assert entry.title == "ACTION"
    assert entry.other_data == "test"
    assert entry.quantity == Money(amount=1.56, currency_code="EUR")
    assert entry.balance == Money(amount=-1.56, currency_code="EUR")


def test_entry_dates_as_time():
    entry = Entry(
        entry_date="01/02/2022",
        date_of_action="03/05/2022",
        title="ACTION",
        other_data="test",
        quantity=Money(amount=1.56, currency_code="EUR"),
        balance=Money(amount=-1.56, currency_code="EUR"),
    )
    assert entry.entry_date == "01/02/2022"
    assert entry.date_of_action == "03/05/2022"
    assert entry.date_as_time() == date(day=1, month=2, year=2022)
    assert entry.month_from_date() == 2
    assert entry.date_of_action_as_time() == date(day=3, month=5, year=2022)
    assert entry.month_from_date_of_action() == 5
