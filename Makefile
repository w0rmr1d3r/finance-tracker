install:
	poetry install --only main

install-dev:
	poetry install

update:
	poetry update

lock:
	poetry lock

lock-refresh:
	poetry lock --no-update

run:
	poetry run python3 finance_tracker/__main__.py

test:
	poetry run pytest -svvvv

lint:
	poetry run isort --check-only .
	poetry run black --check finance_tracker/ tests/
	poetry run flake8 finance_tracker/ tests/

py-lint:
	poetry run pylint finance_tracker/

py-lint-test:
	poetry run pylint --disable=C0116 tests/

format:
	poetry run isort --float-to-top .
	poetry run black finance_tracker/ tests/

build:
	poetry build

.PHONY: install install-dev update lock lock-refresh run setup-test test lint py-lint py-lint-test format build
