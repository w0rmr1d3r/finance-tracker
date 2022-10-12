from collections import defaultdict

from deprecated.classic import deprecated

from finance_tracker.entries.categorized_entry import CategorizedEntry
from finance_tracker.money.money import DEFAULT_MONEY, Money
from finance_tracker.printer import bcolors


class AggregatorByMonth:
    INT_MONTH_TO_STR_CONVERTER = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December",
    }

    @deprecated(reason="Typo in name, use <int_month_to_str> instead", version="0.1.0")
    def int_mont_to_str(self, month: int) -> str:
        return self.int_month_to_str(month)

    def int_month_to_str(self, month: int) -> str:
        return self.INT_MONTH_TO_STR_CONVERTER.get(month)

    def aggregate_by_month(self, entries: list[CategorizedEntry]) -> dict[dict[str, Money]]:
        # {"January": {"CAT1": 1.0, "CAT2": 2.0}, "February": {"CAT3": 1.0, "CAT4": 2.0}}
        if entries is None:
            bcolors.print_warning("WARNING - entries are <None>. Will fail to aggregate them.")
            return {}

        months = defaultdict(dict, {v: defaultdict(Money) for k, v in self.INT_MONTH_TO_STR_CONVERTER.items()})
        for entry in entries:
            month_of_entry = self.int_mont_to_str(entry.month_from_date())
            months[month_of_entry][entry.category] = (
                months[month_of_entry].get(entry.category, DEFAULT_MONEY) + entry.quantity
            )

        return months
