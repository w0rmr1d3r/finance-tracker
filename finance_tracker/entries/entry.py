from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class Entry:
    entry_date: str
    date_of_action: str
    title: str
    other_data: str
    quantity: float
    balance: float

    def date_as_time(self) -> date:
        return datetime.strptime(self.entry_date, "%d/%m/%Y").date()

    def date_of_action_as_time(self) -> date:
        return datetime.strptime(self.date_of_action, "%d/%m/%Y").date()

    def month_from_date(self) -> int:
        return self.date_as_time().month

    def month_from_date_of_action(self) -> int:
        return self.date_of_action_as_time().month
