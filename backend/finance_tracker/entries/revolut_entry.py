from dataclasses import dataclass
from datetime import date, datetime

from finance_tracker.constants import DATE_AS_TIME_FORMAT, DATE_FORMAT
from finance_tracker.money.currency_codes import CurrencyCodes
from finance_tracker.money.money import Money


@dataclass
class RevolutEntry:
    """Represents a raw entry read from a Revolut CSV export."""

    type: str
    product: str
    started_date: str
    completed_date: str
    description: str
    amount: float
    fee: float
    currency: str
    state: str
    balance: float

    def quantity(self) -> Money:
        """
        Returns the quantity of this entry as a Money object composed of
        the same amount and currency code from its currency.
        :return: Money from amount and currency
        """
        return Money(amount=self.amount, currency_code=CurrencyCodes[self.currency])

    def balance_as_money(self) -> Money:
        """
        Return the balance as a Money object.

        :return: Money from balance and currency
        """
        return Money(amount=self.balance, currency_code=CurrencyCodes[self.currency])

    def started_date_as_time(self) -> date:
        """
        Return started_date parsed as a date object.

        :return: Date object from started_date
        """
        return datetime.strptime(self.started_date, DATE_AS_TIME_FORMAT).date()

    def started_date_for_entry(self) -> str:
        """
        Return started_date formatted as day/month/year string.

        :return: Formatted started_date string
        """
        return self.started_date_as_time().strftime(DATE_FORMAT)

    def completed_date_as_time(self) -> date:
        """
        Return completed_date parsed as a date object.

        :return: Date object from completed_date
        """
        return datetime.strptime(self.completed_date, DATE_AS_TIME_FORMAT).date()

    def completed_date_for_entry(self) -> str:
        """
        Return completed_date formatted as day/month/year string.

        :return: Formatted completed_date string
        """
        return self.completed_date_as_time().strftime(DATE_FORMAT)

    def month_from_started_date(self) -> int:
        """
        Return the numeric month from started_date.

        :return: Month number of started_date
        """
        return self.started_date_as_time().month

    def month_from_completed_date_of_action(self) -> int:
        """
        Return the numeric month from completed_date.

        :return: Month number of completed_date
        """
        return self.completed_date_as_time().month
