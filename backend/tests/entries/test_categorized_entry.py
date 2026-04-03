from finance_tracker.entries.categorized_entry import CategorizedEntry
from finance_tracker.money.money import Money


def test_categorized_entry_can_be_built():
    entry = CategorizedEntry(
        entry_date="01/01/2022",
        date_of_action="01/01/2022",
        title="ACTION",
        other_data="test",
        quantity=Money(amount=1.56, currency_code="EUR"),
        balance=Money(amount=-1.56, currency_code="EUR"),
        category="RANDOM",
    )
    assert entry.entry_date == "01/01/2022"
    assert entry.date_of_action == "01/01/2022"
    assert entry.title == "ACTION"
    assert entry.other_data == "test"
    assert entry.quantity == Money(amount=1.56, currency_code="EUR")
    assert entry.balance == Money(amount=-1.56, currency_code="EUR")
    assert entry.category == "RANDOM"


def test_categorized_entry_can_be_built_with_default_category_from_an_entry(entry):
    categorized_entry = CategorizedEntry.from_entry_with_default_category(entry)
    assert categorized_entry.entry_date == "01/02/2022"
    assert categorized_entry.date_of_action == "03/05/2022"
    assert categorized_entry.title == "ACTION"
    assert categorized_entry.other_data == "test"
    assert categorized_entry.quantity == Money(amount=1.56, currency_code="EUR")
    assert categorized_entry.balance == Money(amount=-1.56, currency_code="EUR")
    assert categorized_entry.category == "n/a"


def test_categorized_entry_can_be_built_with_a_category_from_an_entry(entry):
    categorized_entry = CategorizedEntry.from_entry_with_category(entry=entry, category="CATEGORY")
    assert categorized_entry.entry_date == "01/02/2022"
    assert categorized_entry.date_of_action == "03/05/2022"
    assert categorized_entry.title == "ACTION"
    assert categorized_entry.other_data == "test"
    assert categorized_entry.quantity == Money(amount=1.56, currency_code="EUR")
    assert categorized_entry.balance == Money(amount=-1.56, currency_code="EUR")
    assert categorized_entry.category == "CATEGORY"
