import json
import pathlib
from typing import Set

from finance_tracker.constants import DEFAULT_CATEGORIES, DEFAULT_CATEGORY, ENCODING


def all_categories():
    """
    Retrieves all the categories from the "categories.json" file.
    If the file weren't found, it will return <DEFAULT_CATEGORIES>

    :return: Python dict retrieved from the categories file
    """
    current_path = pathlib.Path(__file__).parent.resolve()
    try:
        with open(f"{current_path}/../../load/categories/categories.json", "r", encoding=ENCODING) as file:
            return json.load(file)
    except FileNotFoundError:
        return DEFAULT_CATEGORIES


def categories_items():
    """
    Return the CATEGORIES dict from the categories file.

    :return: Dict mapping category names to lists of keywords
    """
    return all_categories().get("CATEGORIES")


def positive_categories() -> Set:
    """
    Return the set of positive (income) category names.

    :return: Set of positive category name strings
    """
    return set(all_categories().get("POSITIVE_CATEGORIES"))


def categories() -> Set:
    """
    Return the set of all category names.

    :return: Set of all category name strings
    """
    return set(categories_items().keys())


def negative_categories() -> Set:
    """
    Return the set of negative (expense) category names including the default.

    :return: Set of negative category name strings
    """
    return set(categories() - positive_categories()).union({DEFAULT_CATEGORY})
