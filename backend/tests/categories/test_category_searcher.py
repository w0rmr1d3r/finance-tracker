from unittest.mock import MagicMock, patch

import pytest

from finance_tracker.categories.category_searcher import CategorySearcher


@pytest.fixture(autouse=True)
def clear_search_cache():
    """Clear the lru_cache before and after each test to prevent cross-test pollution."""
    CategorySearcher.search_category.cache_clear()
    yield
    CategorySearcher.search_category.cache_clear()


@patch("finance_tracker.categories.categories.all_categories")
def test_category_searcher_returns_na_if_category_not_found(patched_all_categories: MagicMock, all_categories):
    patched_all_categories.return_value = all_categories
    searcher = CategorySearcher()
    result = searcher.search_category(title="random")
    assert result == "n/a"


@patch("finance_tracker.categories.categories.all_categories")
def test_category_searcher_returns_a_category_if_category_category_for_title_exists(
    patched_all_categories: MagicMock, all_categories
):
    patched_all_categories.return_value = all_categories
    searcher = CategorySearcher()
    result = searcher.search_category(title="PAYCHECK_FROM_COMPANY")
    assert result == "PAYCHECK"


@patch("finance_tracker.categories.categories.all_categories")
def test_cache_clear_forces_re_evaluation_after_category_assignment(patched_all_categories: MagicMock):
    """cache_clear() must be called after updating categories.json so that newly assigned
    titles are re-categorised on the next _save_entries() run (fixes the stale-cache bug)."""
    patched_all_categories.return_value = {"CATEGORIES": {}, "POSITIVE_CATEGORIES": []}
    assert CategorySearcher.search_category(title="AMAZON") == "n/a"

    # Simulate adding "AMAZON" to "SHOPPING" in categories.json
    patched_all_categories.return_value = {"CATEGORIES": {"SHOPPING": ["AMAZON"]}, "POSITIVE_CATEGORIES": []}

    # Without clearing the cache the old result is still returned
    assert CategorySearcher.search_category(title="AMAZON") == "n/a"

    # After cache_clear() the updated categories are picked up
    CategorySearcher.search_category.cache_clear()
    assert CategorySearcher.search_category(title="AMAZON") == "SHOPPING"
