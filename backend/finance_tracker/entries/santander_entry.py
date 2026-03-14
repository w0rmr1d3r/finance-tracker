from dataclasses import dataclass

from finance_tracker.money.currency_codes import CurrencyCodes
from finance_tracker.money.money import Money


@dataclass
class SantanderEntry:
    """Represents a raw entry read from a Santander CSV export."""

    operation_date: str
    value_date: str
    concept: str
    amount: float
    balance: float

    def quantity(self) -> Money:
        """
        Return the entry amount as a Money object in EUR.

        :return: Money from amount in EUR
        """
        return Money(amount=self.amount, currency_code=CurrencyCodes["EUR"])

    def balance_as_money(self) -> Money:
        """
        Return the balance as a Money object in EUR.

        :return: Money from balance in EUR
        """
        return Money(amount=self.balance, currency_code=CurrencyCodes["EUR"])
