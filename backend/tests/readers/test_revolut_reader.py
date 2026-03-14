import pathlib

import pytest

from finance_tracker.readers.revolut_reader import RevolutReader


@pytest.fixture
def reader() -> RevolutReader:
    return RevolutReader()


def test_revolut_reader_reads_a_revolut_entry(reader):
    current_path = pathlib.Path(__file__).parent.resolve()
    path_to_file = f"{current_path}/files/test_revolut_reader_one_entry.csv"
    result = reader.read_from_file(path_to_file=path_to_file)

    assert len(result) == 1
    assert result[0].type == "CARD_PAYMENT"
    assert result[0].product == "Current"
    assert result[0].started_date == "2022-10-02 15:01:02"
    assert result[0].completed_date == "2022-10-03 15:01:02"
    assert result[0].description == "Supermarket purchase"
    assert result[0].amount == -4
    assert result[0].fee == 0
    assert result[0].currency == "EUR"
    assert result[0].state == "COMPLETED"
    assert result[0].balance == 100


def test_revolut_reader_reads_several_revolut_entries(reader):
    current_path = pathlib.Path(__file__).parent.resolve()
    path_to_file = f"{current_path}/files/test_revolut_reader_several_entries.csv"
    result = reader.read_from_file(path_to_file=path_to_file)

    assert len(result) == 10


def test_revolut_reader_does_nothing_on_empty_file(reader):
    current_path = pathlib.Path(__file__).parent.resolve()
    path_to_file = f"{current_path}/files/test_revolut_reader_no_entries.csv"
    result = reader.read_from_file(path_to_file=path_to_file)

    assert len(result) == 0
