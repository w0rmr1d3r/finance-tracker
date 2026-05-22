# finance-tracker

Full-stack web app to track and visualise finances over a year.

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/w0rmr1d3r/finance-tracker)](https://github.com/w0rmr1d3r/finance-tracker/releases)
[![GHA](https://github.com/w0rmr1d3r/finance-tracker/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/w0rmr1d3r/finance-tracker/actions/workflows/main.yml)
![GitHub last commit](https://img.shields.io/github/last-commit/w0rmr1d3r/finance-tracker)

## Usage

1. Create the needed folders by running the script `setup.sh`.
    - `config/` — `categories.json` plus the JSON files the server writes
    - `load_data/` — drop your CSV exports here (any bank, all in this folder)

2. Run with Docker Compose:

```yaml
services:
  finance-tracker:
    image: ghcr.io/w0rmr1d3r/finance-tracker:latest
    ports:
      - "80:80"
    volumes:
      - ./config:/app/config
      - ./load_data:/app/load_data
    restart: unless-stopped
```

3. Open <http://localhost>

## Banks supported and CSV format

The bank format is detected from each CSV's header line. Drop every file directly in
`load_data/`.

### Revolut

```csv
Type,Product,Started Date,Completed Date,Description,Amount,Fee,Currency,State,Balance
Transfer,Current,2026-01-17 00:55:20,2026-01-17 00:55:20,Transfer from X,51.50,0.00,EUR,COMPLETED,50.00
```

### Santander

Comma-delimited (current export):

```csv
FECHA OPERACIÓN,FECHA VALOR,CONCEPTO,IMPORTE EUR,SALDO
28/01/2026,28/01/2026,Transferencia De X,50.00,50.00
```

Semicolon-delimited with European decimals (legacy export) is also accepted.

### Trading212

```csv
Action,Time,ISIN,Ticker,Name,Notes,ID,No. of shares,Price / share,Currency (Price / share),Exchange rate,Result,Currency (Result),Total,Currency (Total),Withholding tax,Currency (Withholding tax),Merchant name,Merchant category,French transaction tax,Currency (French transaction tax)
Interest on cash,2026-01-01 02:06:08,,,,Interest on cash,...,0.01,EUR,,,,,,
```

### Default (any other bank)

Fallback used when the header doesn't match the formats above. Comma-delimited:

```csv
DATE,TITLE,DESCRIPTION,QUANTITY
01/01/1999,PAYCHECK,PAYCHECK FROM COMPANY 1,100.00
```

Semicolon-delimited with European decimals (`1000,00`) is also accepted — the delimiter
is detected automatically from the header.

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for development setup, the API reference, and
Makefile targets.

## License

[MIT](https://choosealicense.com/licenses/mit/)
