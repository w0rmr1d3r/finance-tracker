from collections import defaultdict

from finance_tracker.entries.categorized_entry import CategorizedEntry
from finance_tracker.printer import bcolors


class AggregatorByMonth:

    INT_MONTH_TO_STR_CONVERTER = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]

    def int_mont_to_str(self, month: int) -> str:
        return self.INT_MONTH_TO_STR_CONVERTER[month - 1]

    def aggregate_by_month(self, entries: list[CategorizedEntry]) -> dict[dict[str, float]]:
        # {"January": {"CAT1": 1.0, "CAT2": 2.0}, "February": {"CAT3": 1.0, "CAT4": 2.0}}
        if entries is None:
            bcolors.print_warning("WARNING - entries are <None>. Will fail to aggregate them.")
            return {}

        months = defaultdict(dict, {k: defaultdict(float) for k in self.INT_MONTH_TO_STR_CONVERTER})
        for entry in entries:
            month_of_entry = self.int_mont_to_str(entry.month_from_date())
            months[month_of_entry][entry.category] = months[month_of_entry].get(entry.category, 0.0) + entry.quantity

        return months
