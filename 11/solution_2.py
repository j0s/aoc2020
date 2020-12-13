#!/usr/bin/env python

import sys
from typing import IO, Any, Optional, List
from enum import Enum
from dataclasses import dataclass

debug: bool = False
logfile: Optional[IO[Any]] = None


def log(msg: str) -> None:
    global logfile
    if debug:
        if logfile is None:
            logfile = open("output", "w")
        logfile.write(msg + "\n")


@dataclass(frozen=True)
class Seat:
    x: int
    y: int


class CoordState(Enum):
    FREE_SEAT = 1
    TAKEN_SEAT = 2
    NO_SEAT = 3


SYMBOL_MAP = {
    "L": CoordState.FREE_SEAT,
    "#": CoordState.TAKEN_SEAT,
    ".": CoordState.NO_SEAT,
}

CHAR_MAP = {
    CoordState.FREE_SEAT: "L",
    CoordState.TAKEN_SEAT: "#",
    CoordState.NO_SEAT: ".",
}


def parse_input(filename: str) -> List[List[CoordState]]:
    seats: List[List[CoordState]] = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            row = []
            for char in line:
                row.append(SYMBOL_MAP[char])
            seats.append(row)
    return seats


def get_surrounding_coords(seat: Seat) -> List[Seat]:
    return [
        Seat(seat.x - 1, seat.y - 1),
        Seat(seat.x - 1, seat.y),
        Seat(seat.x - 1, seat.y + 1),
        Seat(seat.x, seat.y - 1),
        Seat(seat.x, seat.y + 1),
        Seat(seat.x + 1, seat.y - 1),
        Seat(seat.x + 1, seat.y),
        Seat(seat.x + 1, seat.y + 1),
    ]


def taken_seen_seats(seats: List[List[CoordState]], seat: Seat) -> int:
    occupied_seats = 0
    # Left up
    for offset, x in enumerate(range(seat.x - 1, -1, -1), 1):
        y = seat.y - offset
        if y < 0 or seats[y][x] == CoordState.FREE_SEAT:
            break
        if seats[y][x] == CoordState.TAKEN_SEAT:
            occupied_seats += 1
            break

    # Left down
    for offset, x in enumerate(range(seat.x - 1, -1, -1), 1):
        y = seat.y + offset
        if y > MAX_Y or seats[y][x] == CoordState.FREE_SEAT:
            break
        if seats[y][x] == CoordState.TAKEN_SEAT:
            occupied_seats += 1
            break

    # Left
    for offset, x in enumerate(range(seat.x - 1, -1, -1), 1):
        if seats[seat.y][x] == CoordState.FREE_SEAT:
            break
        if seats[seat.y][x] == CoordState.TAKEN_SEAT:
            occupied_seats += 1
            break

    # Right up
    for offset, x in enumerate(range(seat.x + 1, MAX_X + 1), 1):
        y = seat.y - offset
        if y < 0 or seats[y][x] == CoordState.FREE_SEAT:
            break
        if seats[y][x] == CoordState.TAKEN_SEAT:
            occupied_seats += 1
            break

    # Right down
    for offset, x in enumerate(range(seat.x + 1, MAX_X + 1), 1):
        y = seat.y + offset
        if y > MAX_Y or seats[y][x] == CoordState.FREE_SEAT:
            break
        if seats[y][x] == CoordState.TAKEN_SEAT:
            occupied_seats += 1
            break

    # Right
    for offset, x in enumerate(range(seat.x + 1, MAX_X + 1), 1):
        if seats[seat.y][x] == CoordState.FREE_SEAT:
            break
        if seats[seat.y][x] == CoordState.TAKEN_SEAT:
            occupied_seats += 1
            break

    # Up
    for y in range(seat.y - 1, -1, -1):
        if seats[y][seat.x] == CoordState.TAKEN_SEAT:
            occupied_seats += 1
            break
        elif seats[y][seat.x] == CoordState.FREE_SEAT:
            break

    # Down
    for y in range(seat.y + 1, MAX_Y + 1):
        if seats[y][seat.x] == CoordState.FREE_SEAT:
            break
        if seats[y][seat.x] == CoordState.TAKEN_SEAT:
            occupied_seats += 1
            break

    return occupied_seats


def will_become_empty(seats: List[List[CoordState]], seat: Seat) -> bool:
    return (
        seats[seat.y][seat.x] == CoordState.TAKEN_SEAT
        and taken_seen_seats(seats, seat) >= 5
    )


def will_become_occupied(seats: List[List[CoordState]], seat: Seat) -> bool:
    return (
        seats[seat.y][seat.x] == CoordState.FREE_SEAT
        and taken_seen_seats(seats, seat) == 0
    )


def do_moves(seats: List[List[CoordState]]) -> int:
    moves = 0
    old_seats = []
    for row in seats:
        old_seats.append(row.copy())
    for y, row in enumerate(old_seats):
        for x, _ in enumerate(row):
            if will_become_empty(old_seats, Seat(x, y)):
                moves += 1
                seats[y][x] = CoordState.FREE_SEAT
            elif will_become_occupied(old_seats, Seat(x, y)):
                moves += 1
                seats[y][x] = CoordState.TAKEN_SEAT
    return moves


def print_seats(seats: List[List[CoordState]]):
    log("seats:")
    for row in seats:
        log("".join([CHAR_MAP[x] for x in row]))


if __name__ == "__main__":
    debug = "--debug" in sys.argv
    seats_input = parse_input(sys.argv[-1])
    MAX_Y = len(seats_input) - 1
    MAX_X = len(seats_input[0]) - 1
    iterations = 0
    while do_moves(seats_input) > 0:
        print_seats(seats_input)
        iterations += 1

    occupied_seats = sum([row.count(CoordState.TAKEN_SEAT) for row in seats_input])
    print(f"iterations: {iterations} " f"occupied seats: {occupied_seats}")
