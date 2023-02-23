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
