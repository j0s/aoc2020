from solution_1 import parse_row, parse_column, get_seat_id, Seat
from dataclasses import dataclass


@dataclass
class Case:
    input: str
    result: Seat
    id: int


tests = [
    Case("FBFBBFFRLR", Seat(44, 5), 357),
    Case("BFFFBBFRRR", Seat(70, 7), 567),
    Case("FFFBBBFRRR", Seat(14, 7), 119),
    Case("BBFFBBFRLL", Seat(102, 4), 820),
]


def test_parse_column() -> None:
    for t in tests:
        assert parse_column(t.input) == t.result.column


def test_parse_row() -> None:
    for t in tests:
        assert parse_row(t.input) == t.result.row


def test_get_seat_id() -> None:
    for t in tests:
        assert get_seat_id(t.result) == t.id
