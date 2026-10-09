from typing import Dict

import pytest

from finance_tracker.entries.entry import Entry
from finance_tracker.entries.revolut_entry import RevolutEntry
from finance_tracker.entries.trade_republic_entry import TradeRepublicEntry
from finance_tracker.entries.trading212_entry import Trading212Entry
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


@pytest.fixture
def trading212_entry() -> Trading212Entry:
    return Trading212Entry(
        action="Card debit",
        time="2024-03-15 10:30:00",
        total=-25.50,
        currency_total="EUR",
        merchant_name="Coffee Shop",
    )


@pytest.fixture
def trading212_entry_time_v2() -> Trading212Entry:
    return Trading212Entry(
        action="Card debit",
        time="2026-06-15 10:30:00+00:00",
        total=-25.50,
        currency_total="EUR",
        merchant_name="Coffee Shop",
    )


@pytest.fixture
def trading212_entry_usd() -> Trading212Entry:
    return Trading212Entry(
        action="Dividend",
        time="2024-01-15 09:00:00",
        total=1.50,
        currency_total="USD",
        merchant_name="",
    )


@pytest.fixture
def trade_republic_entry() -> TradeRepublicEntry:
    return TradeRepublicEntry(
        type="BUY",
        datetime="2026-08-03T07:48:42.436Z",
        amount=-50.00,
        fee=-1.00,
        tax=0.0,
        currency="EUR",
    )


@pytest.fixture
def trade_republic_entry_dividend() -> TradeRepublicEntry:
    return TradeRepublicEntry(
        type="DIVIDEND",
        datetime="2026-08-13T07:57:33.508421Z",
        amount=0.04,
        fee=0.0,
        tax=-0.02,
        currency="EUR",
    )
