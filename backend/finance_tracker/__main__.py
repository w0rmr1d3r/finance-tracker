import json
import logging
import os
import pathlib
from contextlib import asynccontextmanager
from json import JSONEncoder

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from finance_tracker.aggregators.aggregator_by_month import AggregatorByMonth
from finance_tracker.categories.categories import (
    DEFAULT_CATEGORY,
    all_categories,
    negative_categories,
    positive_categories,
)
from finance_tracker.categories.categorizer import Categorizer
from finance_tracker.categories.category_searcher import CategorySearcher
from finance_tracker.entries.entry import Entry
from finance_tracker.readers.entry_reader import EntryReader
from finance_tracker.readers.revolut_reader import RevolutReader
from finance_tracker.readers.santander_reader import SantanderReader

logger = logging.getLogger(__name__)


def read_entries_from_files(entries):
    """
    Read CSV entries in the generic/default format from the entries_files directory into entries.

    :param entries: List to extend with the read Entry objects
    """
    logger.info("Searching for Default entries files...")
    current_path = pathlib.Path(__file__).parent.resolve()
    entries_files = os.listdir(f"{current_path}/../load/entries_files/")
    logger.info(f"Found: {len(entries_files) - 1} files")
    reader = EntryReader()
    logger.info("Reading entries from files...")
    for file in entries_files:
        if file.endswith(".csv"):
            entries.extend(
                reader.read_from_file(
                    path_to_file=f"{current_path}/../load/entries_files/{file}",
                )
            )


def read_revolut_entries_from_files(revolut_entries):
    """
    Read Revolut CSV entries from the revolut sub-directory into revolut_entries.

    :param revolut_entries: List to extend with the read RevolutEntry objects
    """
    logger.info("Searching for Revolut files...")
    current_path = pathlib.Path(__file__).parent.resolve()
    revolut_entries_files = os.listdir(f"{current_path}/../load/entries_files/revolut/")
    logger.info(f"Found: {len(revolut_entries_files) - 1} Revolut files")
    revolut_reader = RevolutReader()
    logger.info("Reading entries from Revolut files...")
    for file in revolut_entries_files:
        if file.endswith(".csv"):
            revolut_entries.extend(
                revolut_reader.read_from_file(
                    path_to_file=f"{current_path}/../load/entries_files/revolut/{file}",
                )
            )


def read_santander_entries_from_files(santander_entries):
    """
    Read Santander CSV entries from the santander sub-directory into santander_entries.

    :param santander_entries: List to extend with the read SantanderEntry objects
    """
    logger.info("Searching for Santander files...")
    current_path = pathlib.Path(__file__).parent.resolve()
    santander_entries_files = os.listdir(f"{current_path}/../load/entries_files/santander/")
    logger.info(f"Found: {len(santander_entries_files) - 1} Santander files")
    santander_reader = SantanderReader()
    logger.info("Reading entries from Santander files...")
    for file in santander_entries_files:
        if file.endswith(".csv"):
            santander_entries.extend(
                santander_reader.read_from_file(
                    path_to_file=f"{current_path}/../load/entries_files/santander/{file}",
                )
            )


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
    read_entries_from_files(entries=entries)

    revolut_entries = []
    read_revolut_entries_from_files(revolut_entries=revolut_entries)

    for rev_entry in revolut_entries:
        entries.append(Entry.from_revolut_entry(rev_entry))

    santander_entries = []
    read_santander_entries_from_files(santander_entries=santander_entries)
    for san_entry in santander_entries:
        entries.append(Entry.from_santander_entry(san_entry))

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
    """Processes entries and writes results to saved_files/."""
    positive_aggregated, negative_aggregated, uncategorized, all_entries = _process_entries()
    saved_files_path = pathlib.Path(__file__).parent.resolve() / ".." / "saved_files"
    saved_files_path.mkdir(parents=True, exist_ok=True)

    with open(saved_files_path / "positive.json", "w", encoding="utf-8") as f:
        json.dump(positive_aggregated, f, ensure_ascii=False, indent=4, cls=FinanceTrackerEncoder)

    with open(saved_files_path / "negative.json", "w", encoding="utf-8") as f:
        json.dump(negative_aggregated, f, ensure_ascii=False, indent=4, cls=FinanceTrackerEncoder)

    with open(saved_files_path / "uncategorized.json", "w", encoding="utf-8") as f:
        json.dump(uncategorized, f, ensure_ascii=False, indent=4, cls=FinanceTrackerEncoder)

    with open(saved_files_path / "all_entries.json", "w", encoding="utf-8") as f:
        json.dump(all_entries, f, ensure_ascii=False, indent=4, cls=FinanceTrackerEncoder)


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: RUF029
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
    saved_files_path = pathlib.Path(__file__).parent.resolve() / ".." / "saved_files"
    positive_path = saved_files_path / "positive.json"
    negative_path = saved_files_path / "negative.json"
    uncategorized_path = saved_files_path / "uncategorized.json"

    if not positive_path.exists() or not negative_path.exists() or not uncategorized_path.exists():
        raise HTTPException(status_code=503, detail="Data not yet available")

    with open(positive_path, "r", encoding="utf-8") as f:
        positive = json.load(f)

    with open(negative_path, "r", encoding="utf-8") as f:
        negative = json.load(f)

    with open(uncategorized_path, "r", encoding="utf-8") as f:
        uncategorized = json.load(f)

    return JSONResponse({"positive": positive, "negative": negative, "uncategorized": uncategorized})


@app.get("/entries")
def get_entries():
    """Reads and returns all individual entries."""
    saved_files_path = pathlib.Path(__file__).parent.resolve() / ".." / "saved_files"
    path = saved_files_path / "all_entries.json"
    if not path.exists():
        raise HTTPException(status_code=503, detail="Entries not yet available")
    with open(path, "r", encoding="utf-8") as f:
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

    categories_path = pathlib.Path(__file__).parent.resolve() / ".." / "load" / "categories" / "categories.json"
    with open(categories_path, "w", encoding="ASCII") as f:
        json.dump(current_cats, f, ensure_ascii=True, indent=4)

    CategorySearcher.search_category.cache_clear()
    _save_entries()

    saved_files_path = pathlib.Path(__file__).parent.resolve() / ".." / "saved_files"
    with open(saved_files_path / "positive.json", "r", encoding="utf-8") as f:
        positive = json.load(f)
    with open(saved_files_path / "negative.json", "r", encoding="utf-8") as f:
        negative = json.load(f)
    with open(saved_files_path / "uncategorized.json", "r", encoding="utf-8") as f:
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

    categories_path = pathlib.Path(__file__).parent.resolve() / ".." / "load" / "categories" / "categories.json"
    with open(categories_path, "w", encoding="ASCII") as f:
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
    categories_path = pathlib.Path(__file__).parent.resolve() / ".." / "load" / "categories" / "categories.json"
    with open(categories_path, "w", encoding="ASCII") as f:
        json.dump(current_cats, f, ensure_ascii=True, indent=4)

    CategorySearcher.search_category.cache_clear()
    _save_entries()

    return JSONResponse(
        {
            "categories": current_cats["CATEGORIES"],
            "positive_categories": current_cats.get("POSITIVE_CATEGORIES", []),
        }
    )
