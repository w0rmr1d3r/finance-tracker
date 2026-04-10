from dataclasses import dataclass
from datetime import date, datetime

from finance_tracker.constants import DATE_FORMAT
from finance_tracker.entries.revolut_entry import RevolutEntry
from finance_tracker.entries.santander_entry import SantanderEntry
from finance_tracker.money.money import Money


@dataclass
class Entry:
    """Represents a financial entry with date, title, quantity, and balance."""

    entry_date: str
    date_of_action: str
    title: str
    other_data: str
    quantity: Money
    balance: Money

    def date_as_time(self) -> date:
        """
        Returns self entry_date converted to a date object

        :return: Date object given an entry_date
        """
        return datetime.strptime(self.entry_date, DATE_FORMAT).date()

    def date_of_action_as_time(self) -> date:
        """
        Returns self date_of_action converted to a date object

        :return: Date object given a date_of_action
        """
        return datetime.strptime(self.date_of_action, DATE_FORMAT).date()

    def month_from_date(self) -> int:
        """
        Return the numeric month from entry_date.

        :return: Month number of entry_date
        """
        return self.date_as_time().month

    def month_from_date_of_action(self) -> int:
        """
        Return the numeric month from date_of_action.

        :return: Month number of date_of_action
        """
        return self.date_of_action_as_time().month

    @classmethod
    def from_santander_entry(cls, santander_entry: SantanderEntry):
        """
        Return an Entry built from a SantanderEntry.

        :param santander_entry: SantanderEntry to obtain data from
        :return: Entry from a SantanderEntry
        """
        return cls(
            entry_date=santander_entry.operation_date,
            date_of_action=santander_entry.value_date,
            title=santander_entry.concept,
            other_data="",
            quantity=santander_entry.quantity(),
            balance=santander_entry.balance_as_money(),
        )

    @classmethod
    def from_revolut_entry(cls, revolut_entry: RevolutEntry):
        """
        Returns an entry from a RevolutEntry. Values not recognized or not being in RevolutEntry will be created
        with default values.
        :param revolut_entry: RevolutEntry to obtain data from
        :return: Entry from a RevolutEntry
        """
        return cls(
            entry_date=revolut_entry.started_date_for_entry(),
            date_of_action=revolut_entry.completed_date_for_entry(),
            title=revolut_entry.description,
            other_data="",
            quantity=revolut_entry.quantity(),
            balance=revolut_entry.balance_as_money(),
        )
