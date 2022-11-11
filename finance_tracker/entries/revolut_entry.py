from dataclasses import dataclass
from datetime import date, datetime

from deprecated.classic import deprecated

from finance_tracker.money.currency_codes import CurrencyCodes
from finance_tracker.money.money import Money


@dataclass
class RevolutEntry:
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

    @deprecated(reason="Use quantity. Entries use the value its read, no absolute.", version="1.1.0")
    def quantity_as_absolute(self) -> Money:
        return Money(amount=abs(self.amount), currency_code=CurrencyCodes[self.currency])

    def balance_as_money(self) -> Money:
        return Money(amount=self.balance, currency_code=CurrencyCodes[self.currency])

    def started_date_as_time(self) -> date:
        return datetime.strptime(self.started_date, "%Y-%m-%d %H:%M:%S").date()

    def started_date_for_entry(self) -> str:
        s_date = self.started_date_as_time()
        return f"{s_date.day}/{s_date.month}/{s_date.year}"

    def completed_date_as_time(self) -> date:
        return datetime.strptime(self.completed_date, "%Y-%m-%d %H:%M:%S").date()

    def completed_date_for_entry(self) -> str:
        c_date = self.completed_date_as_time()
        return f"{c_date.day}/{c_date.month}/{c_date.year}"

    def month_from_started_date(self) -> int:
        return self.started_date_as_time().month

    def month_from_completed_date_of_action(self) -> int:
        return self.completed_date_as_time().month
