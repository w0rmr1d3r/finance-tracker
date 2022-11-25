import json
import pathlib
from typing import Set

DEFAULT_CATEGORY = "n/a"


def all_categories():
    """
    Retrieves all the categories from the "categories.json" file.

    :return: Python dict retrieved from the categories file
    """
    current_path = pathlib.Path(__file__).parent.resolve()
    with open(f"{current_path}/../../load/categories/categories.json", "r", encoding="ASCII") as file:
        return json.load(file)


def categories_items():
    return all_categories().get("CATEGORIES")


def positive_categories() -> Set:
    return set(all_categories().get("POSITIVE_CATEGORIES"))


def categories() -> Set:
    return set(categories_items().keys())


def negative_categories() -> Set:
    return set(categories() - positive_categories()).union({DEFAULT_CATEGORY})
