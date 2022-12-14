from unittest.mock import MagicMock, patch

from finance_tracker.categories.categorizer import Categorizer
from finance_tracker.categories.category_searcher import CategorySearcher
from finance_tracker.entries.entry import Entry
from finance_tracker.money.money import Money


@patch("finance_tracker.categories.categories.all_categories")
def test_it_transforms_an_entry_to_a_categorized_entry(patched_all_categories: MagicMock, all_categories, entry):
    patched_all_categories.return_value = all_categories
    category_searcher = CategorySearcher()
    categorizer = Categorizer(category_searcher=category_searcher)
    result = categorizer.set_category_for_entry(uncategorized_entry=entry)
    assert result.category == "n/a"


@patch("finance_tracker.categories.categories.all_categories")
def test_it_transforms_a_list_of_entries_to_a_list_of_categorized_entries(
    patched_all_categories: MagicMock, all_categories, entry
):
    patched_all_categories.return_value = all_categories
    category_searcher = CategorySearcher()
    categorizer = Categorizer(category_searcher=category_searcher)
    entries = [
        entry,
        Entry(
            entry_date="01/01/2022",
            date_of_action="01/01/2022",
            title="ACTION_TWO",
            other_data="test",
            quantity=Money(amount=1.56, currency_code="EUR"),
            balance=Money(amount=-1.56, currency_code="EUR"),
        ),
    ]
    categorizer.set_category_for_entries(uncategorized_entries=entries)
    assert entries[0].category == "n/a"
    assert entries[1].category == "n/a"
