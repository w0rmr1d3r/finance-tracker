from dataclasses import dataclass

from finance_tracker.categories.categories import DEFAULT_CATEGORY
from finance_tracker.entries.entry import Entry


@dataclass
class CategorizedEntry(Entry):
    category: str

    @classmethod
    def from_entry_with_default_category(cls, entry: Entry):
        """
        Returns a CategorizedEntry with DEFAULT_CATEGORY given an Entry object

        :param entry: Entry object to convert to a CategorizedEntry
        :return: CategorizedEntry with DEFAULT_CATEGORY
        """
        return cls(**entry.__dict__, category=DEFAULT_CATEGORY)

    @classmethod
    def from_entry_with_category(cls, entry: Entry, category: str):
        """
        Returns a CategorizedEntry with a category given an Entry object and a category

        :param entry: Entry object to convert to a CategorizedEntry
        :param category: Category str value
        :return: CategorizedEntry object
        """
        return cls(**entry.__dict__, category=category)
