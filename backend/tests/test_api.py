"""Tests for the FastAPI endpoints in finance_tracker.__main__."""

import json
from unittest.mock import MagicMock, mock_open, patch

import pytest
from fastapi.testclient import TestClient

from finance_tracker.categories.category_searcher import CategorySearcher

SAMPLE_CATS = {
    "CATEGORIES": {
        "GROCERIES": ["supermarket"],
        "SALARY": ["paycheck"],
    },
    "POSITIVE_CATEGORIES": ["SALARY"],
}


@pytest.fixture()
def client():
    """Return a TestClient with lifespan (startup _save_entries) suppressed."""
    with patch("finance_tracker.__main__._save_entries"):
        from finance_tracker.__main__ import app  # noqa: PLC0415, PLC2701

        with TestClient(app, raise_server_exceptions=True) as c:
            yield c


# ---------------------------------------------------------------------------
# DELETE /categories/{name}
# ---------------------------------------------------------------------------


def test_delete_unknown_category_returns_404(client):
    with patch("finance_tracker.__main__.all_categories", return_value={"CATEGORIES": {}, "POSITIVE_CATEGORIES": []}):
        resp = client.delete("/categories/NONEXISTENT")
    assert resp.status_code == 404


def test_delete_expense_category_removes_it_and_calls_save_entries(client):
    cats = {
        "CATEGORIES": {"GROCERIES": ["supermarket"], "SALARY": ["paycheck"]},
        "POSITIVE_CATEGORIES": ["SALARY"],
    }

    m = mock_open()
    with (
        patch("finance_tracker.__main__.all_categories", return_value=cats),
        patch("builtins.open", m),
        patch("finance_tracker.__main__._save_entries") as mock_save,
        patch.object(CategorySearcher.search_category, "cache_clear") as mock_cc,
    ):
        resp = client.delete("/categories/GROCERIES")

    assert resp.status_code == 200
    body = resp.json()
    assert "GROCERIES" not in body["categories"]
    assert "SALARY" in body["categories"]
    assert body["positive_categories"] == ["SALARY"]
    mock_save.assert_called_once()
    mock_cc.assert_called_once()


def test_delete_income_category_removes_from_positive_categories_and_calls_save_entries(client):
    cats = {
        "CATEGORIES": {"GROCERIES": ["supermarket"], "SALARY": ["paycheck"]},
        "POSITIVE_CATEGORIES": ["SALARY"],
    }

    m = mock_open()
    with (
        patch("finance_tracker.__main__.all_categories", return_value=cats),
        patch("builtins.open", m),
        patch("finance_tracker.__main__._save_entries") as mock_save,
        patch.object(CategorySearcher.search_category, "cache_clear") as mock_cc,
    ):
        resp = client.delete("/categories/SALARY")

    assert resp.status_code == 200
    body = resp.json()
    assert "SALARY" not in body["categories"]
    assert "SALARY" not in body["positive_categories"]
    mock_save.assert_called_once()
    mock_cc.assert_called_once()


def test_delete_category_persists_updated_json(client):
    """Verify categories.json is written, cache is cleared, then _save_entries is called."""
    cats = {
        "CATEGORIES": {"GROCERIES": ["supermarket"]},
        "POSITIVE_CATEGORIES": [],
    }

    written_data = {}
    call_order = []

    def fake_open(path, mode="r", **kwargs):
        path_str = str(path)
        if "categories.json" in path_str and "w" in mode:
            handle = MagicMock()
            handle.__enter__ = lambda s: s
            handle.__exit__ = MagicMock(return_value=False)

            def capture_write(data):
                written_data["content"] = data

            handle.write = capture_write
            call_order.append("open")
            return handle
        raise FileNotFoundError(path)

    def fake_save():
        call_order.append("save")

    def fake_cache_clear():
        call_order.append("cache_clear")

    with (
        patch("finance_tracker.__main__.all_categories", return_value=cats),
        patch("builtins.open", side_effect=fake_open),
        patch("json.dump", side_effect=lambda obj, *a, **kw: None),
        patch("finance_tracker.__main__._save_entries", side_effect=fake_save),
        patch.object(CategorySearcher.search_category, "cache_clear", side_effect=fake_cache_clear),
    ):
        resp = client.delete("/categories/GROCERIES")

    assert resp.status_code == 200
    assert call_order == ["open", "cache_clear", "save"], (
        "categories.json must be written, then cache cleared, then _save_entries called"
    )


# ---------------------------------------------------------------------------
# POST /categories/assign — existing behaviour; _save_entries already called
# ---------------------------------------------------------------------------


def test_assign_category_calls_save_entries(client):
    cats = {
        "CATEGORIES": {"GROCERIES": []},
        "POSITIVE_CATEGORIES": [],
    }
    saved = {
        "positive": [],
        "negative": [],
        "uncategorized": [],
    }

    def fake_open(path, mode="r", **kwargs):
        path_str = str(path)
        handle = MagicMock()
        handle.__enter__ = lambda s: s
        handle.__exit__ = MagicMock(return_value=False)
        if "categories.json" in path_str and "w" in mode:
            handle.write = MagicMock()
            return handle
        if any(k in path_str for k in ("positive.json", "negative.json", "uncategorized.json")):
            key = next(k for k in ("positive", "negative", "uncategorized") if k in path_str)
            handle.read = MagicMock(return_value=json.dumps(saved[key]))
            return handle
        raise FileNotFoundError(path)

    with (
        patch("finance_tracker.__main__.all_categories", return_value=cats),
        patch("builtins.open", side_effect=fake_open),
        patch("json.dump", side_effect=lambda obj, *a, **kw: None),
        patch("json.load", side_effect=lambda f: []),
        patch("finance_tracker.__main__._save_entries") as mock_save,
        patch.object(CategorySearcher.search_category, "cache_clear") as mock_cc,
    ):
        resp = client.post("/categories/assign", json={"title": "supermarket", "category": "GROCERIES"})

    assert resp.status_code == 200
    mock_save.assert_called_once()
    mock_cc.assert_called_once()
