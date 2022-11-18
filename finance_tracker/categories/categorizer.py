from finance_tracker.categories.category_searcher import CategorySearcher
from finance_tracker.entries.categorized_entry import CategorizedEntry
from finance_tracker.entries.entry import Entry


class Categorizer:
    def __init__(self, category_searcher: CategorySearcher):
        self.category_searcher = category_searcher

    def set_category_for_entry(self, uncategorized_entry: Entry) -> CategorizedEntry:
        """
        Given an Entry object, it returns a CategorizedEntry with its right category after being searched.

        :param uncategorized_entry: Entry object to convert to a CategorizedEntry
        :return: CategorizedEntry object
        """
        category = self.category_searcher.search_category(title=uncategorized_entry.title)
        return CategorizedEntry.from_entry_with_category(entry=uncategorized_entry, category=category)

    def set_category_for_entries(self, uncategorized_entries: list[Entry]) -> None:
        """
        Given a list of Entry objects, converts each entry of the list to a CategorizedEntry.

        :param uncategorized_entries: list of Entry objects
        :return: None, the list will have different objects in it
        """
        for i in range(len(uncategorized_entries)):
            uncategorized_entries[i] = self.set_category_for_entry(uncategorized_entries[i])
