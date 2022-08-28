from collections import defaultdict

from finance_tracker.entries.categorized_entry import CategorizedEntry


class CategoriesQuantityAggregator:
    @staticmethod
    def aggregate_by_category(entries: list[CategorizedEntry]) -> dict[str, float]:
        categories_quantities = defaultdict(float)
        if entries is None:
            # warn logger here
            return categories_quantities

        for entry in entries:
            categories_quantities[entry.category] = categories_quantities.get(entry.category, 0.0) + entry.quantity
        return categories_quantities
