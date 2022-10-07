# finance-tracker

Python tool to track finances over a year

## Installation

### PyPi package

TBD

## Usage

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

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
