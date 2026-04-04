# finance-tracker

Full-stack web app to track and visualise finances over a year.

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/w0rmr1d3r/finance-tracker)](https://github.com/w0rmr1d3r/finance-tracker/releases)
[![GHA](https://github.com/w0rmr1d3r/finance-tracker/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/w0rmr1d3r/finance-tracker/actions/workflows/main.yml)
![GitHub last commit](https://img.shields.io/github/last-commit/w0rmr1d3r/finance-tracker)

## Project structure

```
finance-tracker/
├── backend/          # FastAPI + Python (uv)
├── frontend/         # React 18 + Vite
└── docker-compose.yml
```

## Usage

### Docker with pre-built images (recommended)

No need to clone the full repo — uses published images from the container registry.

1. Install [Docker](https://docs.docker.com/get-docker/)
2. Download `docker-compose-example.yml` from this repo and rename it `docker-compose.yml`
3. Run `setup.sh` to create the required directory structure and a starter `categories.json`:
   ```bash
   bash setup.sh
   ```
4. Edit the `volumes` paths in `docker-compose.yml` to point to the `backend/load` and `backend/saved_files` directories
   created by the script (use absolute paths)
5. Set up the data as explained [here](#setting-up-the-data)
6. Run `docker compose up -d`
7. Open the UI at `http://localhost` and the API at `http://localhost:8000`

### Docker (from source)

1. Clone the repo
2. Install [Docker](https://docs.docker.com/get-docker/)
3. Run `setup.sh` to create the required directory structure:
   ```bash
   bash setup.sh
   ```
4. Set up the data as explained [here](#setting-up-the-data)
5. Run `make docker-build` and then `make docker-run`
6. Open the UI at `http://localhost` and the API at `http://localhost:8000`

#### Startup behaviour

On startup the backend server automatically processes all entries and writes four files under `backend/saved_files/`:

- `positive.json` — income entries aggregated by month and category
- `negative.json` — expense entries aggregated by month and category
- `uncategorized.json` — entries that did not match any category keyword
- `all_entries.json` — every individual entry (all banks combined)

#### API endpoints

- `GET /data` — returns aggregated income, expenses, and uncategorized entries:
    ```json
    {
      "positive": { "<month>": { "<category>": { "_amount": "...", "_currency_code": "..." } } },
      "negative": { "<month>": { "<category>": { "_amount": "...", "_currency_code": "..." } } },
      "uncategorized": [ { "entry_date": "...", "title": "...", "other_data": "...", "quantity": { "_amount": "...", "_currency_code": "..." } } ]
    }
    ```
- `GET /entries` — returns all individual entries across all banks
- `GET /categories` — returns the current category definitions and which are income categories
- `POST /categories/assign` — assigns an entry title to a category and re-processes entries
    ```json
    { "title": "ENTRY TITLE", "category": "CATEGORY_NAME" }
    ```
- `POST /categories/create` — creates a new category
    ```json
    { "name": "CATEGORY_NAME", "type": "expense" }
    ```
- `DELETE /categories/{name}` — deletes a category and re-processes entries

### From repository (local)

#### Backend

1. Clone the repo
2. Install [uv](https://docs.astral.sh/uv/)
3. Run `make install`
4. Set up the data as explained [here](#setting-up-the-data)
5. Run `uvicorn finance_tracker.__main__:app --host 0.0.0.0 --port 8000` from `backend/`

#### Frontend

1. Install [Node.js](https://nodejs.org/) 20+
2. Run `make frontend-install`
3. Run `cd frontend && npm run dev` — served at `http://localhost:5173`

## Setting up the data

1. Run `setup.sh` to create the required directory structure (skip if you already ran it during setup):
   ```bash
   bash setup.sh
   ```

2. Drop your CSV files into `./backend/load/entries_files/` — either directly (default format) or under a bank
   subfolder (e.g. `revolut/`, `santander/`). See [Banks supported](#banks-supported).
   Default CSV format:
    ```csv
    DATE;TITLE;DESCRIPTION;QUANTITY
    01/01/1999;PAYCHECK;PAYCHECK FROM COMPANY 1;1000,00
    ```

3. `./backend/load/categories/categories.json` is created empty by `setup.sh` — you can leave it as-is and categorise entries later
   via the UI, or pre-fill it:
    ```json
    {
      "CATEGORIES": {
        "CATEGORY_ONE": ["TITLE TO CATEGORIZE"],
        "CATEGORY_TWO": ["TITLE 2 TO CATEGORIZE"]
      },
      "POSITIVE_CATEGORIES": ["CATEGORY_TWO"]
    }
    ```
   Each category maps entry title keywords to a category name. Categories in `POSITIVE_CATEGORIES` are treated as
   income; all others as expenses.

## Banks supported

- Revolut
- Santander

Any other bank can be supported by implementing a new reader or by formatting your export as the default CSV (see
[Setting up the data](#setting-up-the-data)).

## Development

### Makefile targets

| Target                  | Description                              |
|-------------------------|------------------------------------------|
| `make install`          | Install backend production dependencies  |
| `make install-dev`      | Install backend development dependencies |
| `make test`             | Run backend tests                        |
| `make lint`             | Lint backend code                        |
| `make format`           | Format backend code                      |
| `make run`              | Run backend locally                      |
| `make lock`             | Lock backend dependencies                |
| `make lock-upgrade`     | Upgrade and re-lock backend dependencies |
| `make frontend-install` | Install frontend dependencies (`npm ci`) |
| `make frontend-test`    | Run frontend tests (Vitest)              |
| `make frontend-build`   | Build frontend for production            |
| `make docker-build`     | Build Docker images                      |
| `make docker-run`       | Start all services via Docker Compose    |

### Running tests

```bash
# Backend
make test

# Frontend
make frontend-test
```

## Contributing

Pull requests are welcome. Issues are welcome too.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
