install:
	uv sync --no-dev --frozen

install-dev:
	uv sync --group dev --frozen

format:
	uv run --frozen ruff check --fix
	uv run --frozen ruff format

lint:
	uv run --frozen ruff check

test:
	uv run --frozen pytest -vvv tests

lock:
	uv lock

lock-upgrade:
	uv lock --upgrade

.PHONY: install install-dev format lint test lock lock-upgrade
