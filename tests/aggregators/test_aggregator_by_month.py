import pytest

from finance_tracker.aggregators.aggregator_by_month import AggregatorByMonth
from finance_tracker.entries.categorized_entry import CategorizedEntry


@pytest.fixture
def aggregator() -> AggregatorByMonth:
    return AggregatorByMonth()


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
            quantity=1000,
            balance=-1.56,
            category="PAYCHECK",
        ),
        CategorizedEntry(
            entry_date="01/02/2022",
            date_of_action="01/02/2022",
            title="ACTION",
            other_data="test",
            quantity=1000.01,
            balance=-1.56,
            category="PAYCHECK",
        ),
    ]

    result = aggregator.aggregate_by_month(entries=entries)
    assert result == {
        "January": {"PAYCHECK": 1000},
        "February": {"PAYCHECK": 1000.01},
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