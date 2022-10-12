import pytest

from finance_tracker.aggregators.categories_quantity_aggregator import CategoriesQuantityAggregator
from finance_tracker.entries.categorized_entry import CategorizedEntry


@pytest.fixture
def aggregator() -> CategoriesQuantityAggregator:
    return CategoriesQuantityAggregator()


@pytest.mark.skip(reason="Deprecated class")
def test_if_no_entries_given_returns_quantities_with_zero(aggregator):
    result = aggregator.aggregate_by_category(entries=[])
    assert result == {}


@pytest.mark.skip(reason="Deprecated class")
def test_if_entries_is_none_returns_quantities_with_zero(aggregator):
    result = aggregator.aggregate_by_category(entries=None)
    assert result == {}


@pytest.mark.skip(reason="Deprecated class")
def test_if_entries_given_returns_aggregated_quantities(aggregator):
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
            entry_date="01/01/2022",
            date_of_action="01/01/2022",
            title="ACTION",
            other_data="test",
            quantity=1000.01,
            balance=-1.56,
            category="PAYCHECK",
        ),
    ]

    result = aggregator.aggregate_by_category(entries=entries)
    assert result == {
        "PAYCHECK": 2000.01,
    }
