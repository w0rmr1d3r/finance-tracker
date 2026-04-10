import pathlib

import pytest

from finance_tracker.readers.santander_reader import SantanderReader


@pytest.fixture
def reader() -> SantanderReader:
    return SantanderReader()


def test_santander_reader_reads_a_santander_entry(reader):
    current_path = pathlib.Path(__file__).parent.resolve()
    path_to_file = f"{current_path}/files/test_santander_reader_one_entry.csv"
    result = reader.read_from_file(path_to_file=path_to_file)

    assert len(result) == 1
    assert result[0].operation_date == "28/01/2026"
    assert result[0].value_date == "28/01/2026"
    assert result[0].concept == "Nomina"
    assert result[0].amount == 1000.00
    assert result[0].balance == 1000.00


def test_santander_reader_reads_several_santander_entries(reader):
    current_path = pathlib.Path(__file__).parent.resolve()
    path_to_file = f"{current_path}/files/test_santander_reader_several_entries.csv"
    result = reader.read_from_file(path_to_file=path_to_file)

    assert len(result) == 10


def test_santander_reader_reads_new_format_entry(reader):
    current_path = pathlib.Path(__file__).parent.resolve()
    path_to_file = f"{current_path}/files/test_santander_reader_one_entry_new_format.csv"
    result = reader.read_from_file(path_to_file=path_to_file)

    assert len(result) == 1
    assert result[0].operation_date == "28/01/2026"
    assert result[0].value_date == "28/01/2026"
    assert result[0].concept == "Nomina"
    assert result[0].amount == 1000.00
    assert result[0].balance == 1000.00


def test_santander_reader_reads_new_format_entry_with_quoted_concept(reader):
    current_path = pathlib.Path(__file__).parent.resolve()
    path_to_file = f"{current_path}/files/test_santander_reader_quoted_concept_new_format.csv"
    result = reader.read_from_file(path_to_file=path_to_file)

    assert len(result) == 1
    assert result[0].operation_date == "24/02/2026"
    assert result[0].value_date == "20/02/2026"
    assert result[0].concept == "CONCEPT WITH , COMAS"
    assert result[0].amount == -4.70
    assert result[0].balance == 1000.00


def test_santander_reader_does_nothing_on_empty_file(reader):
    current_path = pathlib.Path(__file__).parent.resolve()
    path_to_file = f"{current_path}/files/test_santander_reader_no_entries.csv"
    result = reader.read_from_file(path_to_file=path_to_file)

    assert len(result) == 0
