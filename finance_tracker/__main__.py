import os
import pathlib

import inquirer
from pandas import DataFrame

from finance_tracker.aggregators.aggregator_by_month import AggregatorByMonth
from finance_tracker.categories.categories import negative_categories, positive_categories
from finance_tracker.categories.categorizer import Categorizer
from finance_tracker.categories.category_searcher import CategorySearcher
from finance_tracker.entries.entry import Entry
from finance_tracker.money.money import DEFAULT_MONEY
from finance_tracker.printer import bcolors
from finance_tracker.readers.entry_reader import EntryReader
from finance_tracker.readers.revolut_reader import RevolutReader


def run():
    # Init objects
    current_path = pathlib.Path(__file__).parent.resolve()
    category_searcher = CategorySearcher()
    categorizer = Categorizer(category_searcher=category_searcher)
    month_aggregator = AggregatorByMonth()
    reader = EntryReader()
    revolut_reader = RevolutReader()

    # Looking for files
    bcolors.print_green("Searching for files...")
    entries_files = os.listdir(f"{current_path}/../load/entries_files/")
    revolut_entries_files = os.listdir(f"{current_path}/../load/entries_files/revolut/")
    bcolors.print_green(f"Found: {len(entries_files) - 1} files")
    bcolors.print_green(f"Found: {len(revolut_entries_files) - 1} Revolut files")

    # Read from files
    bcolors.print_green("Reading entries from files...")
    entries = []
    for file in entries_files:
        if file.endswith(".csv"):
            entries.extend(
                reader.read_from_file(
                    path_to_file=f"{current_path}/../load/entries_files/{file}",
                )
            )

    # Reading from Revolut files
    bcolors.print_green("Reading entries from Revolut files...")
    revolut_entries = []
    for file in revolut_entries_files:
        if file.endswith(".csv"):
            revolut_entries.extend(
                revolut_reader.read_from_file(
                    path_to_file=f"{current_path}/../load/entries_files/revolut/{file}",
                )
            )

    # We transform Revolut entries to Entry
    for rev_entry in revolut_entries:
        entries.append(Entry.from_revolut_entry(rev_entry))

    bcolors.print_green("Setting categories for entries...")
    categorizer.set_category_for_entries(uncategorized_entries=entries)

    bcolors.print_green("Splitting entries into positives and negatives")
    positive = [entry for entry in entries if entry.category in positive_categories()]
    negative = [entry for entry in entries if entry.category in negative_categories()]

    bcolors.print_green("Aggregating entries by month...")
    positive_categories_quantities = month_aggregator.aggregate_by_month(entries=positive)
    negative_categories_quantities = month_aggregator.aggregate_by_month(entries=negative)

    bcolors.print_cyan("\nResult is:\n")
    bcolors.print_fail(
        DataFrame.from_dict(
            data=negative_categories_quantities,
            orient="columns",
        ).fillna(DEFAULT_MONEY)
    )
    print("-" * 100)
    bcolors.print_green(
        DataFrame.from_dict(
            data=positive_categories_quantities,
            orient="columns",
        ).fillna(DEFAULT_MONEY)
    )
    print("\n\n")


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
