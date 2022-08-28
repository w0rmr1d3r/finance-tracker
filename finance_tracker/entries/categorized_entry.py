from dataclasses import dataclass

from finance_tracker.categories.categories import DEFAULT_CATEGORY
from finance_tracker.entries.entry import Entry


@dataclass
class CategorizedEntry(Entry):
    category: str

    @classmethod
    def from_entry_with_default_category(cls, entry: Entry):
        return cls(**entry.__dict__, category=DEFAULT_CATEGORY)

    @classmethod
    def from_entry_with_category(cls, entry: Entry, category: str):
        return cls(**entry.__dict__, category=category)
