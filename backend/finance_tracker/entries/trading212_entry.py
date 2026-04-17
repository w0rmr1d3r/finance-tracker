from dataclasses import dataclass
from datetime import date, datetime

from finance_tracker.constants import DATE_AS_TIME_FORMAT, DATE_FORMAT
from finance_tracker.money.currency_codes import CurrencyCodes
from finance_tracker.money.money import Money


@dataclass
class Trading212Entry:
    """Represents a raw entry read from a Trading212 CSV export."""

    action: str
    time: str
    total: float
    currency_total: str
    merchant_name: str

    def quantity(self) -> Money:
        """
        Return the total as a Money object using the Currency (Total) column.

        :return: Money from total and currency_total
        """
        return Money(amount=self.total, currency_code=CurrencyCodes[self.currency_total])

    def time_as_date(self) -> date:
        """
        Return the time field parsed as a date object.

        :return: Date object from time
        """
        return datetime.strptime(self.time, DATE_AS_TIME_FORMAT).date()

    def time_for_entry(self) -> str:
        """
        Return the time formatted as day/month/year string.

        :return: Formatted time string
        """
        return self.time_as_date().strftime(DATE_FORMAT)
