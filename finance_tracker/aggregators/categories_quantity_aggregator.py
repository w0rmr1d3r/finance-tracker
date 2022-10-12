from collections import defaultdict

from deprecated.classic import deprecated

from finance_tracker.entries.categorized_entry import CategorizedEntry


@deprecated(reason="Use <AggregatorByMonth> instead, this isn't being used", version="0.1.0")
class CategoriesQuantityAggregator:
    @staticmethod
    def aggregate_by_category(entries: list[CategorizedEntry]) -> dict[str, float]:
        categories_quantities = defaultdict(float)
        if entries is None:
            # warn logger here
            return categories_quantities

        for entry in entries:
            categories_quantities[entry.category] = (
                categories_quantities.get(entry.category, 0.0) + entry.quantity.amount
            )
        return categories_quantities
