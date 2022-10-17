from dataclasses import dataclass
from datetime import date, datetime

from finance_tracker.money.currency_codes import CurrencyCodes
from finance_tracker.money.money import Money


@dataclass
class RevolutEntry:
    type: str
    product: str
    started_date: str
    completed_date: str
    description: str
    amount: float  # todo - this includes sign eg -4, careful when grouping by categories, needs to be updated
    fee: float
    currency: str
    state: str
    balance: float

    def quantity(self) -> Money:
        return Money(amount=self.amount, currency_code=CurrencyCodes[self.currency])

    def started_date_as_time(self) -> date:
        return datetime.strptime(self.started_date, "%Y-%m-%d %H:%M:%S").date()

    def completed_date_as_time(self) -> date:
        return datetime.strptime(self.completed_date, "%Y-%m-%d %H:%M:%S").date()

    def month_from_started_date(self) -> int:
        return self.started_date_as_time().month

    def month_from_completed_date_of_action(self) -> int:
        return self.completed_date_as_time().month
