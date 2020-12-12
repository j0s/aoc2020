#!/usr/bin/env python

import sys
from typing import IO, Any, List, Optional, Dict
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


def parse_input(filename: str) -> Dict[Seat, bool]:
    seats: Dict[Seat, bool] = {}
    with open(filename, "r") as f:
        for i, line in enumerate(f):
            line = line.strip()
            for j, char in enumerate(line):
                if char == "L":
                    seats[Seat(i, j)] = False
                elif char == "#":
                    seats[Seat(i, j)] = True
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


def will_become_empty(
    seats: Dict[Seat, bool], seat: Seat, max_x: int, max_y: int
) -> bool:
    occupied_seats = 0
    for x in range(seat.x - 1, -1, -1):
        for y in range(seat.y - 1, -1, -1):
            if seats[Seat(x, y)] is True:
                occupied_seats += 1
                break
        for y in range(seat.y + 1, max_y + 1):
            if seats[Seat(x, y)] is True:
                occupied_seats += 1
                break
    return occupied_seats >= 5


def will_become_occupied(seats: Dict[Seat, bool], seat: Seat) -> bool:
    return (
        len(
            [s for s in get_surrounding_coords(seat) if s in seats and seats[s] is True]
        )
        == 0
    )


def do_moves(seats: Dict[Seat, bool], max_x: int, max_y: int) -> int:
    moves = 0
    old_seats = seats.copy()
    for seat, taken in old_seats.items():
        if taken and will_become_empty(old_seats, seat, max_x, max_y):
            log(f"{seat} will become free")
            moves += 1
            seats[seat] = not taken
        if not taken and will_become_occupied(old_seats, seat):
            log(f"{seat} will become occupied")
            moves += 1
            seats[seat] = not taken
    return moves


if __name__ == "__main__":
    debug = "--debug" in sys.argv
    seats_input = parse_input(sys.argv[-1])
    max_x = max(seats_input.keys(), key=lambda s: s.x).x
    max_y = max(seats_input.keys(), key=lambda s: s.y).y
    print(seats_input)
    iterations = 0
    while do_moves(seats_input, max_x, max_y) > 0:
        iterations += 1
    print(
        f"iterations: {iterations} "
        f"occupied seats: {len([1 for _, occupied in seats_input.items() if occupied])}"
    )
    print(seats_input)
