import os
import pathlib

import inquirer
from pandas import DataFrame

from finance_tracker.aggregators.aggregator_by_month import AggregatorByMonth
from finance_tracker.categories.categories import negative_categories, positive_categories
from finance_tracker.categories.categorizer import Categorizer
from finance_tracker.categories.category_searcher import CategorySearcher
from finance_tracker.printer import bcolors
from finance_tracker.readers.entry_reader import EntryReader


def run():
    current_path = pathlib.Path(__file__).parent.resolve()
    category_searcher = CategorySearcher()
    categorizer = Categorizer(category_searcher=category_searcher)
    month_aggregator = AggregatorByMonth()
    reader = EntryReader()

    bcolors.print_green("Searching for files...")
    entries_files = os.listdir(f"{current_path}/../load/entries_files/")
    bcolors.print_green(f"Found: {len(entries_files)} files")

    bcolors.print_green("Reading entries from files...")
    entries = []
    for file in entries_files:
        if file.endswith(".csv"):
            entries.extend(
                reader.read_entries_from_file(
                    headers_to_ignore=3,
                    path_to_file=f"{current_path}/../load/entries_files/{file}",
                )
            )

    bcolors.print_green("Setting categories for entries...")
    categorizer.set_category_for_entries(uncategorized_entries=entries)

    bcolors.print_green("Splitting categories into positive vs negative")
    positive = [entry for entry in entries if entry.category in positive_categories()]
    negative = [entry for entry in entries if entry.category in negative_categories()]

    bcolors.print_green("Aggregating entries by month...")
    positive_categories_quantities = month_aggregator.aggregate_by_month(entries=positive)
    negative_categories_quantities = month_aggregator.aggregate_by_month(entries=negative)

    bcolors.print_cyan("\nResult is:\n")
    print(
        DataFrame.from_dict(
            data=negative_categories_quantities,
            orient="columns",
        ).fillna(0.0)
    )
    print("-" * 100)
    print(
        DataFrame.from_dict(
            data=positive_categories_quantities,
            orient="columns",
        ).fillna(0.0)
    )
    bcolors.print_cyan("\n\n")


def menu():
    last_choice = None
    while True:
        choice = inquirer.list_input("", choices=["run", "exit"], default=last_choice)
        if choice == "run":
            run()
        elif choice == "exit":
            return 0
        last_choice = choice


if __name__ == "__main__":
    menu()
