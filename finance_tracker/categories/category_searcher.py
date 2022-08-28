from functools import cache

from finance_tracker.categories.categories import CATEGORIES_ITEMS, DEFAULT_CATEGORY
from finance_tracker.printer import bcolors


class CategorySearcher:
    @cache
    def search_category(self, title: str) -> str:
        for category, categorized_items in CATEGORIES_ITEMS.items():
            if title in categorized_items:
                return category
        bcolors.print_warning(f"WARNING - No category detected for title <{title}>, proceeding with default")
        return DEFAULT_CATEGORY
