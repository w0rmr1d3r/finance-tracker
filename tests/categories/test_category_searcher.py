import time

from finance_tracker.categories.category_searcher import CategorySearcher


def test_category_searcher_returns_na_if_category_not_found():
    searcher = CategorySearcher()
    result = searcher.search_category(title="random")
    assert result == "n/a"


def test_category_searcher_returns_a_category_if_category_category_for_title_exists():
    searcher = CategorySearcher()
    result = searcher.search_category(title="NOMINA")
    assert result == "PAYCHECK"


def test_category_searcher_cache_works():
    """
    If the cache of the searcher gets deleted, this test still passes :shrug:
    It may need a better way to check it works.
    todo - the better way is to test this,
    by searching for a category, let's say, 500 times and see that the print/logger
    only outputs once that it hasn't found a category
    """
    searcher = CategorySearcher()
    first_time_start = time.time()
    searcher.search_category(title="NOMINA")
    first_time_end = time.time()
    searcher.search_category(title="NOMINA")
    second_time_end = time.time()
    assert (second_time_end - first_time_end) <= (first_time_end - first_time_start)
