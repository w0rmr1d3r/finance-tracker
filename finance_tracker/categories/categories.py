import json
import pathlib

current_path = pathlib.Path(__file__).parent.resolve()
DEFAULT_CATEGORY = "n/a"

with open(f"{current_path}/../../load/categories/categories.json") as f:
    all_categories = json.load(f)
    CATEGORIES_ITEMS = all_categories.get("CATEGORIES")
    POSITIVE_CATEGORIES = set(all_categories.get("POSITIVE_CATEGORIES"))

CATEGORIES = set(CATEGORIES_ITEMS.keys())
NEGATIVE_CATEGORIES = set(CATEGORIES - POSITIVE_CATEGORIES).union({DEFAULT_CATEGORY})
