import pytest

from finance_tracker.aggregators.aggregator_by_month import AggregatorByMonth
from finance_tracker.entries.categorized_entry import CategorizedEntry
from finance_tracker.money.currency_codes import CurrencyCodes
from finance_tracker.money.money import Money


@pytest.fixture
def aggregator() -> AggregatorByMonth:
    return AggregatorByMonth()


@pytest.mark.parametrize(
    "int_month, expected_month",
    [
        (1, "January"),
        (2, "February"),
        (3, "March"),
        (4, "April"),
        (5, "May"),
        (6, "June"),
        (7, "July"),
        (8, "August"),
        (9, "September"),
        (10, "October"),
        (11, "November"),
        (12, "December"),
        (13, None),
    ],
)
def test_get_int_month_to_str(aggregator, int_month, expected_month):
    assert aggregator.int_month_to_str(int_month) == expected_month


def test_if_no_entries_given_returns_quantities_with_zero(aggregator):
    result = aggregator.aggregate_by_month(entries=[])
    assert result == {
        "January": {},
        "February": {},
        "March": {},
        "April": {},
        "May": {},
        "June": {},
        "July": {},
        "August": {},
        "September": {},
        "October": {},
        "November": {},
        "December": {},
    }


def test_if_entries_is_none_returns_quantities_with_zero(aggregator):
    result = aggregator.aggregate_by_month(entries=None)
    assert result == {}


def test_if_entries_given_returns_aggregated_by_month(aggregator):
    entries = [
        CategorizedEntry(
            entry_date="01/01/2022",
            date_of_action="01/01/2022",
            title="ACTION",
            other_data="test",
            quantity=Money(amount=1000, currency_code=CurrencyCodes.EUR),
            balance=Money(amount=-1.56, currency_code=CurrencyCodes.EUR),
            category="PAYCHECK",
        ),
        CategorizedEntry(
            entry_date="01/02/2022",
            date_of_action="01/02/2022",
            title="ACTION",
            other_data="test",
            quantity=Money(amount=1000.01, currency_code=CurrencyCodes.EUR),
            balance=Money(amount=-1.56, currency_code=CurrencyCodes.EUR),
            category="PAYCHECK",
        ),
    ]

    result = aggregator.aggregate_by_month(entries=entries)
    assert result == {
        "January": {"PAYCHECK": Money(amount=1000, currency_code=CurrencyCodes.EUR)},
        "February": {"PAYCHECK": Money(amount=1000.01, currency_code=CurrencyCodes.EUR)},
        "March": {},
        "April": {},
        "May": {},
        "June": {},
        "July": {},
        "August": {},
        "September": {},
        "October": {},
        "November": {},
        "December": {},
    }
