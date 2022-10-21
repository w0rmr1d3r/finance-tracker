from typing import Dict

import pytest

from finance_tracker.entries.entry import Entry
from finance_tracker.entries.revolut_entry import RevolutEntry
from finance_tracker.money.money import Money


@pytest.fixture
def all_categories() -> Dict:
    return {
        "CATEGORIES": {"PAYCHECK": ["PAYCHECK_FROM_COMPANY"]},
        "POSITIVE_CATEGORIES": [],
    }


@pytest.fixture
def entry() -> Entry:
    return Entry(
        entry_date="01/02/2022",
        date_of_action="03/05/2022",
        title="ACTION",
        other_data="test",
        quantity=Money(amount=1.56, currency_code="EUR"),
        balance=Money(amount=-1.56, currency_code="EUR"),
    )


@pytest.fixture
def revolut_entry() -> RevolutEntry:
    return RevolutEntry(
        type="CARD_PAYMENT",
        product="Current",
        started_date="2022-10-02 15:01:02",
        completed_date="2022-10-03 15:01:02",
        description="Supermarket purchase",
        amount=-4,
        fee=0,
        currency="EUR",
        state="COMPLETED",
        balance=100,
    )
