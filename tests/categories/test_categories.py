from finance_tracker.categories.categories import all_categories


def test_all_categories_returns_default_categories_if_file_is_not_found():
    assert {"CATEGORIES": {}, "POSITIVE_CATEGORIES": []} == all_categories()
