# Contributing

Pull requests and issues are welcome. Please update tests as appropriate.

## Project structure

```
finance-tracker/
├── backend/          # FastAPI + Python (uv)
├── frontend/         # React + Vite
├── Dockerfile        # Single image: nginx + uvicorn under supervisord
├── nginx.conf        # Serves the built frontend, proxies /data /categories /entries
├── supervisord.conf  # Runs uvicorn (127.0.0.1:8000) and nginx (:80)
└── docker-compose.yml
```

## Local development

### Backend

1. Install [uv](https://docs.astral.sh/uv/)
2. From the repo root, run `bash setup.sh` to create `config/` and `load_data/`
3. Drop your CSVs into `load_data/`
4. From `backend/`: `make install`
5. From `backend/`: `uvicorn finance_tracker.__main__:app --host 0.0.0.0 --port 8000`

The backend resolves `config/` and `load_data/` from the repo root by default. Override
with `FT_CONFIG_DIR` and `FT_LOAD_DATA_DIR` env vars if needed.

### Frontend

1. Install [Node.js](https://nodejs.org/) 20+
2. From `frontend/`: `make install`
3. From `frontend/`: `npm run dev` — served at <http://localhost:5173>

### Docker (from source)

```bash
make docker-build
make docker-run
```

Open <http://localhost>.

## Startup behaviour

On startup the backend processes all CSVs in `load_data/` and writes four JSON files
into `config/`:

- `positive.json` — income entries aggregated by month and category
- `negative.json` — expense entries aggregated by month and category
- `uncategorized.json` — entries that did not match any category keyword
- `all_entries.json` — every individual entry (all banks combined)

## API reference

- `GET /data` — aggregated income, expenses, and uncategorized entries:
    ```json
    {
      "positive": { "<month>": { "<category>": { "_amount": "...", "_currency_code": "..." } } },
      "negative": { "<month>": { "<category>": { "_amount": "...", "_currency_code": "..." } } },
      "uncategorized": [ { "entry_date": "...", "title": "...", "other_data": "...", "quantity": { "_amount": "...", "_currency_code": "..." } } ]
    }
    ```
- `GET /entries` — all individual entries across all banks
- `GET /categories` — current category definitions and which are income categories
- `POST /categories/assign` — assign an entry title to a category and re-process entries
    ```json
    { "title": "ENTRY TITLE", "category": "CATEGORY_NAME" }
    ```
- `POST /categories/create` — create a new category
    ```json
    { "name": "CATEGORY_NAME", "type": "expense" }
    ```
- `DELETE /categories/{name}` — delete a category and re-process entries

## Categories file format

`config/categories.json`:

```json
{
  "CATEGORIES": {
    "CATEGORY_ONE": ["TITLE TO CATEGORIZE"],
    "CATEGORY_TWO": ["TITLE 2 TO CATEGORIZE"]
  },
  "POSITIVE_CATEGORIES": ["CATEGORY_TWO"]
}
```

Each category maps entry-title keywords to a category name. Categories listed in
`POSITIVE_CATEGORIES` are treated as income; all others as expenses.

## Makefile targets

| Target                  | Description                              |
|-------------------------|------------------------------------------|
| `make install`          | Installs production dependencies         |
| `make install-dev`      | Installs development dependencies        |
| `make test`             | Runs backend and frontend tests          |
| `make lint`             | Lint backend (ruff) and frontend (eslint) |
| `make format`           | Format backend code (ruff)               |
| `make lock`             | Locks dependencies                       |
| `make lock-upgrade`     | Upgrade and re-lock backend dependencies |
| `make frontend-build`   | Build frontend for production            |
| `make docker-build`     | Build the unified Docker image           |
| `make docker-run`       | Start the app via Docker Compose         |

## Running tests

```bash
make test
```
