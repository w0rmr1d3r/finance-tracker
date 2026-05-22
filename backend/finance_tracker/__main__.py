import json
import logging
from contextlib import asynccontextmanager
from json import JSONEncoder

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from finance_tracker.aggregators.aggregator_by_month import AggregatorByMonth
from finance_tracker.categories.categories import (
    all_categories,
    negative_categories,
    positive_categories,
)
from finance_tracker.categories.categorizer import Categorizer
from finance_tracker.categories.category_searcher import CategorySearcher
from finance_tracker.constants import CATEGORIES_FILE, CONFIG_DIR, DEFAULT_CATEGORY, ENCODING, LOAD_DATA_DIR
from finance_tracker.readers.reader_dispatcher import read_into_entries

logger = logging.getLogger(__name__)


def read_entries_from_load_data(entries):
    """
    Read every CSV file in LOAD_DATA_DIR, auto-detecting the bank format from the
    header line, and append generic Entry objects to entries.

    :param entries: List to extend with the read Entry objects
    """
    if not LOAD_DATA_DIR.exists():
        logger.warning("load_data directory not found at %s", LOAD_DATA_DIR)
        return

    csv_files = sorted(p for p in LOAD_DATA_DIR.iterdir() if p.is_file() and p.suffix.lower() == ".csv")
    logger.info("Found %d CSV files in load_data/", len(csv_files))

    for path in csv_files:
        try:
            read_into_entries(str(path), entries)
        except Exception:
            logger.exception("Failed to read %s", path)


class FinanceTrackerEncoder(JSONEncoder):
    """JSON encoder that serialises objects via their __dict__."""

    def default(self, o):  # noqa: PLR6301
        """
        Return o.__dict__ for serialisation.

        :param o: Object to serialise
        :return: Dict representation of the object
        """
        return o.__dict__


def _process_entries():
    category_searcher = CategorySearcher()
    categorizer = Categorizer(category_searcher=category_searcher)
    month_aggregator = AggregatorByMonth()

    entries = []
    read_entries_from_load_data(entries=entries)

    logger.info("Setting categories for entries...")
    categorizer.set_category_for_entries(uncategorized_entries=entries)

    logger.info("Splitting entries into positives, negatives, and uncategorized")
    uncategorized = [entry for entry in entries if entry.category == DEFAULT_CATEGORY]
    positive = [entry for entry in entries if entry.category in positive_categories()]
    negative = [
        entry for entry in entries if entry.category in negative_categories() and entry.category != DEFAULT_CATEGORY
    ]

    logger.info("Aggregating entries by month...")
    positive_aggregated = month_aggregator.aggregate_by_month(entries=positive)
    negative_aggregated = month_aggregator.aggregate_by_month(entries=negative)

    return positive_aggregated, negative_aggregated, uncategorized, entries


def _save_entries():
    """Processes entries and writes results to CONFIG_DIR."""
    positive_aggregated, negative_aggregated, uncategorized, all_entries = _process_entries()
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    with open(CONFIG_DIR / "positive.json", "w", encoding=ENCODING) as f:
        json.dump(positive_aggregated, f, ensure_ascii=False, indent=4, cls=FinanceTrackerEncoder)

    with open(CONFIG_DIR / "negative.json", "w", encoding=ENCODING) as f:
        json.dump(negative_aggregated, f, ensure_ascii=False, indent=4, cls=FinanceTrackerEncoder)

    with open(CONFIG_DIR / "uncategorized.json", "w", encoding=ENCODING) as f:
        json.dump(uncategorized, f, ensure_ascii=False, indent=4, cls=FinanceTrackerEncoder)

    with open(CONFIG_DIR / "all_entries.json", "w", encoding=ENCODING) as f:
        json.dump(all_entries, f, ensure_ascii=False, indent=4, cls=FinanceTrackerEncoder)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Processes and saves entries on server startup."""
    logger.info("Starting up: processing and saving entries...")
    _save_entries()
    logger.info("Startup complete.")
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",  # nginx (production, Docker)
        "http://localhost:5173",  # Vite dev server (local development)
        "http://localhost:80",
    ],
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)


@app.get("/data")
def data():
    """Reads and returns the saved aggregated results."""
    positive_path = CONFIG_DIR / "positive.json"
    negative_path = CONFIG_DIR / "negative.json"
    uncategorized_path = CONFIG_DIR / "uncategorized.json"

    if not positive_path.exists() or not negative_path.exists() or not uncategorized_path.exists():
        raise HTTPException(status_code=503, detail="Data not yet available")

    with open(positive_path, "r", encoding=ENCODING) as f:
        positive = json.load(f)

    with open(negative_path, "r", encoding=ENCODING) as f:
        negative = json.load(f)

    with open(uncategorized_path, "r", encoding=ENCODING) as f:
        uncategorized = json.load(f)

    return JSONResponse({"positive": positive, "negative": negative, "uncategorized": uncategorized})


@app.get("/entries")
def get_entries():
    """Reads and returns all individual entries."""
    path = CONFIG_DIR / "all_entries.json"
    if not path.exists():
        raise HTTPException(status_code=503, detail="Entries not yet available")
    with open(path, "r", encoding=ENCODING) as f:
        return JSONResponse(json.load(f))


@app.get("/categories")
def get_categories():
    """Returns the categories structure from categories.json."""
    cats = all_categories()
    return JSONResponse(
        {
            "categories": cats.get("CATEGORIES", {}),
            "positive_categories": list(cats.get("POSITIVE_CATEGORIES", [])),
        }
    )


class AssignCategoryRequest(BaseModel):
    """Request body for assigning a title to an existing category."""

    title: str
    category: str


class CreateCategoryRequest(BaseModel):
    """Request body for creating a new category."""

    name: str
    type: str  # "income" or "expense"


@app.post("/categories/assign")
def assign_category(req: AssignCategoryRequest):
    """Assigns a title to a category, rewrites categories.json, re-processes entries."""
    current_cats = all_categories()
    existing_categories = set(current_cats.get("CATEGORIES", {}).keys())

    if req.category not in existing_categories:
        raise HTTPException(status_code=400, detail=f"Unknown category: {req.category}")

    cats_dict = current_cats.get("CATEGORIES", {})
    keywords = cats_dict.get(req.category, [])
    if req.title not in keywords:
        keywords.append(req.title)
    cats_dict[req.category] = keywords

    current_cats["CATEGORIES"] = cats_dict

    with open(CATEGORIES_FILE, "w", encoding=ENCODING) as f:
        json.dump(current_cats, f, ensure_ascii=True, indent=4)

    _save_entries()

    with open(CONFIG_DIR / "positive.json", "r", encoding=ENCODING) as f:
        positive = json.load(f)
    with open(CONFIG_DIR / "negative.json", "r", encoding=ENCODING) as f:
        negative = json.load(f)
    with open(CONFIG_DIR / "uncategorized.json", "r", encoding=ENCODING) as f:
        uncategorized = json.load(f)

    return JSONResponse({"positive": positive, "negative": negative, "uncategorized": uncategorized})


@app.post("/categories/create")
def create_category(req: CreateCategoryRequest):
    """Creates a new category in categories.json."""
    name = req.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Category name cannot be empty")
    if req.type not in {"income", "expense"}:
        raise HTTPException(status_code=400, detail="type must be 'income' or 'expense'")

    current_cats = all_categories()
    if name in current_cats.get("CATEGORIES", {}):
        raise HTTPException(status_code=400, detail=f"Category already exists: {name}")

    current_cats["CATEGORIES"][name] = []
    if req.type == "income":
        pos = current_cats.get("POSITIVE_CATEGORIES", [])
        if name not in pos:
            pos.append(name)
        current_cats["POSITIVE_CATEGORIES"] = pos

    with open(CATEGORIES_FILE, "w", encoding=ENCODING) as f:
        json.dump(current_cats, f, ensure_ascii=True, indent=4)

    return JSONResponse(
        {
            "categories": current_cats["CATEGORIES"],
            "positive_categories": current_cats.get("POSITIVE_CATEGORIES", []),
        }
    )


@app.delete("/categories/{name}")
def delete_category(name: str):
    """Deletes a category from categories.json."""
    current_cats = all_categories()
    if name not in current_cats.get("CATEGORIES", {}):
        raise HTTPException(status_code=404, detail=f"Category not found: {name}")

    del current_cats["CATEGORIES"][name]

    pos = current_cats.get("POSITIVE_CATEGORIES", [])
    if name in pos:
        pos.remove(name)
    current_cats["POSITIVE_CATEGORIES"] = pos
    with open(CATEGORIES_FILE, "w", encoding=ENCODING) as f:
        json.dump(current_cats, f, ensure_ascii=True, indent=4)

    _save_entries()

    return JSONResponse(
        {
            "categories": current_cats["CATEGORIES"],
            "positive_categories": current_cats.get("POSITIVE_CATEGORIES", []),
        }
    )
