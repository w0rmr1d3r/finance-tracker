import json
import os
import pathlib
from json import JSONEncoder

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


def read_entries_from_files(entries):
    bcolors.print_green("Searching for Default entries files...")
    current_path = pathlib.Path(__file__).parent.resolve()
    entries_files = os.listdir(f"{current_path}/../load/entries_files/")
    bcolors.print_green(f"Found: {len(entries_files) - 1} files")
    reader = EntryReader()
    bcolors.print_green("Reading entries from files...")
    for file in entries_files:
        if file.endswith(".csv"):
            entries.extend(
                reader.read_from_file(
                    path_to_file=f"{current_path}/../load/entries_files/{file}",
                )
            )


def read_revolut_entries_from_files(revolut_entries):
    bcolors.print_green("Searching for Revolut files...")
    current_path = pathlib.Path(__file__).parent.resolve()
    revolut_entries_files = os.listdir(f"{current_path}/../load/entries_files/revolut/")
    bcolors.print_green(f"Found: {len(revolut_entries_files) - 1} Revolut files")
    revolut_reader = RevolutReader()
    bcolors.print_green("Reading entries from Revolut files...")
    for file in revolut_entries_files:
        if file.endswith(".csv"):
            revolut_entries.extend(
                revolut_reader.read_from_file(
                    path_to_file=f"{current_path}/../load/entries_files/revolut/{file}",
                )
            )


def run() -> None:
    """
    Runs the app.

    :return: None
    """
    # Init objects
    category_searcher = CategorySearcher()
    categorizer = Categorizer(category_searcher=category_searcher)
    month_aggregator = AggregatorByMonth()

    # Read from files
    entries = []
    read_entries_from_files(entries=entries)

    # Reading from Revolut files
    revolut_entries = []
    read_revolut_entries_from_files(revolut_entries=revolut_entries)

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


class FinanceTrackerEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


def save_to_files():
    # Init objects
    category_searcher = CategorySearcher()
    categorizer = Categorizer(category_searcher=category_searcher)
    month_aggregator = AggregatorByMonth()

    # Read from files
    entries = []
    read_entries_from_files(entries=entries)

    # Reading from Revolut files
    revolut_entries = []
    read_revolut_entries_from_files(revolut_entries=revolut_entries)

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

    with open("saved_files/positive.json", "w", encoding="utf-8") as f:
        json.dump(positive_categories_quantities, f, ensure_ascii=False, indent=4, cls=FinanceTrackerEncoder)

    with open("saved_files/negative.json", "w", encoding="utf-8") as f:
        json.dump(negative_categories_quantities, f, ensure_ascii=False, indent=4, cls=FinanceTrackerEncoder)


def menu() -> None:
    """
    Shows the menu with current options of the app.
    Each option should call a function besides exit.

    :return: None
    """
    last_choice = None
    while True:
        choice = inquirer.list_input("", choices=["run", "Save to files", "exit"], default=last_choice)
        if choice == "run":
            run()
        elif choice == "Save to files":
            save_to_files()
        elif choice == "exit":
            return
        last_choice = choice


if __name__ == "__main__":
    menu()
