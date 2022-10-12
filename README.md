# finance-tracker

Python tool to track finances over a year

[![PyPI](https://img.shields.io/pypi/v/finance-tracker)](https://pypi.org/project/finance-tracker/)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/w0rmr1d3r/finance-tracker)](https://github.com/w0rmr1d3r/finance-tracker/releases)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/finance-tracker)
[![CI](https://github.com/w0rmr1d3r/finance-tracker/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/w0rmr1d3r/finance-tracker/actions/workflows/ci.yml)
![GitHub last commit](https://img.shields.io/github/last-commit/w0rmr1d3r/finance-tracker)
[![PyPi downloads](https://img.shields.io/pypi/dm/finance-tracker?label=PyPi%20downloads)](https://pypistats.org/packages/finance-tracker)

## Installation

### PyPi package

```bash
pip install finance-tracker
```

## Usage

### From repository

1. Clone the repo
2. Install poetry
3. Run `make install`
4. Load the categories and categories to filter as incomes wanted in a file called `categories.json`
   in `./load/categories/`. Such as:

    ```json
    {
      "CATEGORIES": {
        "CATEGORY_ONE": [
          "TITLE TO CATEGORIZE"
        ],
        "CATEGORY_TWO": [
          "TITLE 2 TO CATEGORIZE"
        ]
      },
      "POSITIVE_CATEGORIES": [
        "CATEGORY_TWO"
      ]
    }
    ```

5. Load the CSV files in the folder `./load/entries_files/`. Those files have 3 _headers_ (2 with text and 1 with column
   titles) and the following columns:

    ```csv
    HEADER1;;;;;
    HEADER2;;;;;
    DATE;DATE TWO;TITLE;OTHER DATA;QUANTITY;OTHER
    01/01/1999;01/01/1999;PAYCHECK;PAYCHECK FROM COMPANY 1;1.000;1.000
    ```

6. Run `make run`

### From package installation

1. Follow the steps in [Installation](#installation)
2. Load the categories and categories to filter as incomes wanted in a file called `categories.json`
   in `./load/categories/`. Such as:

    ```json
    {
      "CATEGORIES": {
        "CATEGORY_ONE": [
          "TITLE TO CATEGORIZE"
        ],
        "CATEGORY_TWO": [
          "TITLE 2 TO CATEGORIZE"
        ]
      },
      "POSITIVE_CATEGORIES": [
        "CATEGORY_TWO"
      ]
    }
    ```

3. Load the CSV files in the folder `./load/entries_files/`. Those files have 3 _headers_ (2 with text and 1 with column
   titles) and the following columns:

    ```csv
    HEADER1;;;;;
    HEADER2;;;;;
    DATE;DATE TWO;TITLE;OTHER DATA;QUANTITY;OTHER
    01/01/1999;01/01/1999;PAYCHECK;PAYCHECK FROM COMPANY 1;1.000;1.000
    ```

4. Import it and use it in your project like this:
    ```python
    from finance_tracker.__main__ import run

    if __name__ == "__main__":
        run()
    ```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
