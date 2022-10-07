from functools import cache

from finance_tracker.categories.categories import DEFAULT_CATEGORY, categories_items
from finance_tracker.printer import bcolors


class CategorySearcher:
    @cache
    def search_category(self, title: str) -> str:
        for category, categorized_items in categories_items().items():
            if title in categorized_items:
                return category
        bcolors.print_warning(f"WARNING - No category detected for title <{title}>, proceeding with default")
        return DEFAULT_CATEGORY
