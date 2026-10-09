from dataclasses import dataclass
from datetime import date, datetime

from finance_tracker.constants import DATE_FORMAT
from finance_tracker.money.currency_codes import CurrencyCodes
from finance_tracker.money.money import Money


@dataclass
class TradeRepublicEntry:
    """Represents a raw entry read from a TradeRepublic CSV export."""

    type: str
    datetime: str
    amount: float
    fee: float
    tax: float
    currency: str

    def quantity(self) -> Money:
        """
        Return the net cash impact of this entry (amount, fee and tax combined)
        as a Money object. TradeRepublic reports fees and taxes as separate
        columns from the gross amount, so they need to be added back to get
        the actual cash movement.

        :return: Money from amount, fee, tax and currency
        """
        total = self.amount + self.fee + self.tax
        return Money(amount=total, currency_code=CurrencyCodes[self.currency])

    def _datetime_as_date(self) -> date:
        """
        Return the datetime field parsed as a date object.

        :return: Date object from datetime
        """
        return datetime.fromisoformat(self.datetime).date()

    def datetime_for_entry(self) -> str:
        """
        Return the datetime formatted as day/month/year string.

        :return: Formatted datetime string
        """
        return self._datetime_as_date().strftime(DATE_FORMAT)
