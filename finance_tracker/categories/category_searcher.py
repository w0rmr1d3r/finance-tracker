from functools import lru_cache

from finance_tracker.categories.categories import DEFAULT_CATEGORY, categories_items
from finance_tracker.printer import bcolors


class CategorySearcher:
    @lru_cache
    def search_category(self, title: str) -> str:
        """
        Searches the title of an entry in the categories. Returns the name of the category the title is in and
        if not found, the DEFAULT_CATEGORY value.

        :param title: Title of the entry
        :return: Name of the category or default category
        """
        for category, categorized_items in categories_items().items():
            if title in categorized_items:
                return category
        bcolors.print_warning(f"WARNING - No category detected for title <{title}>, proceeding with default")
        return DEFAULT_CATEGORY
