from datetime import date

from finance_tracker.entries.entry import Entry


def test_entry_can_be_built():
    entry = Entry(
        entry_date="01/01/2022",
        date_of_action="01/01/2022",
        title="ACTION",
        other_data="test",
        quantity=1.56,
        balance=-1.56,
    )
    assert entry.entry_date == "01/01/2022"
    assert entry.date_of_action == "01/01/2022"
    assert entry.title == "ACTION"
    assert entry.other_data == "test"
    assert entry.quantity == 1.56
    assert entry.balance == -1.56


def test_entry_dates_as_time():
    entry = Entry(
        entry_date="01/02/2022",
        date_of_action="03/05/2022",
        title="ACTION",
        other_data="test",
        quantity=1.56,
        balance=-1.56,
    )
    assert entry.entry_date == "01/02/2022"
    assert entry.date_of_action == "03/05/2022"
    assert entry.date_as_time() == date(day=1, month=2, year=2022)
    assert entry.month_from_date() == 2
    assert entry.date_of_action_as_time() == date(day=3, month=5, year=2022)
    assert entry.month_from_date_of_action() == 5
