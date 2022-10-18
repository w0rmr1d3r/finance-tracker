import time
from unittest.mock import MagicMock, patch

from finance_tracker.categories.category_searcher import CategorySearcher


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
def test_category_searcher_cache_works(patched_all_categories: MagicMock, all_categories):
    patched_all_categories.return_value = all_categories
    searcher = CategorySearcher()
    first_time_start = time.time()
    searcher.search_category(title="PAYCHECK_FROM_COMPANY")
    first_time_end = time.time()

    for _ in range(500):
        second_time_start = time.time()
        searcher.search_category(title="PAYCHECK_FROM_COMPANY")
        second_time_end = time.time()
        assert (second_time_end - second_time_start) <= (first_time_end - first_time_start)
