from finance_tracker.categories.category_searcher import CategorySearcher
from finance_tracker.entries.categorized_entry import CategorizedEntry
from finance_tracker.entries.entry import Entry


class Categorizer:
    def __init__(self, category_searcher: CategorySearcher):
        self.category_searcher = category_searcher

    def set_category_for_entry(self, uncategorized_entry: Entry) -> CategorizedEntry:
        category = self.category_searcher.search_category(title=uncategorized_entry.title)
        return CategorizedEntry.from_entry_with_category(entry=uncategorized_entry, category=category)

    def set_category_for_entries(self, uncategorized_entries: list[Entry]):
        for i in range(len(uncategorized_entries)):
            uncategorized_entries[i] = self.set_category_for_entry(uncategorized_entries[i])
