from dataclasses import dataclass
from datetime import date, datetime

from finance_tracker.entries.revolut_entry import RevolutEntry
from finance_tracker.money.money import Money


@dataclass
class Entry:
    entry_date: str
    date_of_action: str
    title: str
    other_data: str
    quantity: Money
    balance: Money

    def date_as_time(self) -> date:
        return datetime.strptime(self.entry_date, "%d/%m/%Y").date()

    def date_of_action_as_time(self) -> date:
        return datetime.strptime(self.date_of_action, "%d/%m/%Y").date()

    def month_from_date(self) -> int:
        return self.date_as_time().month

    def month_from_date_of_action(self) -> int:
        return self.date_of_action_as_time().month

    @classmethod
    def from_revolut_entry(cls, revolut_entry: RevolutEntry):
        return cls(
            entry_date=revolut_entry.started_date_for_entry(),
            date_of_action=revolut_entry.completed_date_for_entry(),
            title=revolut_entry.description,
            other_data="",
            quantity=revolut_entry.quantity_as_absolute(),
            balance=revolut_entry.balance_as_money(),
        )
