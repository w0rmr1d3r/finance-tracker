import os
import pathlib

DATE_FORMAT = "%d/%m/%Y"
DATE_AS_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


DEFAULT_CATEGORY = "n/a"
DEFAULT_CATEGORIES = {"CATEGORIES": {}, "POSITIVE_CATEGORIES": []}


ENCODING = "UTF-8"


_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent

CONFIG_DIR = pathlib.Path(os.environ.get("FT_CONFIG_DIR", str(_REPO_ROOT / "config")))
LOAD_DATA_DIR = pathlib.Path(os.environ.get("FT_LOAD_DATA_DIR", str(_REPO_ROOT / "load_data")))

CATEGORIES_FILE = CONFIG_DIR / "categories.json"
