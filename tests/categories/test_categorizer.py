from finance_tracker.categories.categorizer import Categorizer
from finance_tracker.categories.category_searcher import CategorySearcher
from finance_tracker.entries.entry import Entry


def test_it_transforms_an_entry_to_a_categorized_entry():
    category_searcher = CategorySearcher()
    categorizer = Categorizer(category_searcher=category_searcher)
    entry = Entry(
        entry_date="01/01/2022",
        date_of_action="01/01/2022",
        title="ACTION",
        other_data="test",
        quantity=1.56,
        balance=-1.56,
    )
    result = categorizer.set_category_for_entry(uncategorized_entry=entry)
    assert result.category == "n/a"


def test_it_transforms_a_list_of_entries_to_a_list_of_categorized_entries():
    category_searcher = CategorySearcher()
    categorizer = Categorizer(category_searcher=category_searcher)
    entries = [
        Entry(
            entry_date="01/01/2022",
            date_of_action="01/01/2022",
            title="ACTION",
            other_data="test",
            quantity=1.56,
            balance=-1.56,
        ),
        Entry(
            entry_date="01/01/2022",
            date_of_action="01/01/2022",
            title="ACTION_TWO",
            other_data="test",
            quantity=1.56,
            balance=-1.56,
        ),
    ]
    categorizer.set_category_for_entries(uncategorized_entries=entries)
    assert entries[0].category == "n/a"
    assert entries[1].category == "n/a"
