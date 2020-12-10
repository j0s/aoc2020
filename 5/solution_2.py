#!/usr/bin/env python

import sys
import math
from typing import IO, Any, Optional, Iterable
from dataclasses import dataclass

debug: bool = False
logfile: Optional[IO[Any]] = None


def log(msg: str) -> None:
    global logfile
    if debug:
        if logfile is None:
            logfile = open("output", "w")
        logfile.write(msg + "\n")


@dataclass
class Seat:
    row: int
    column: int


def parse_input(filename: str) -> Iterable[Seat]:
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            yield Seat(parse_row(line), parse_column(line))


@dataclass
class Interval:
    lower: int
    upper: int


def apply_bsp_oper(oper: str, interval: Interval) -> Interval:
    if oper in "FL":
        return Interval(
            interval.lower,
            interval.upper - math.ceil((interval.upper - interval.lower) / 2),
        )
    elif oper in "BR":
        return Interval(
            interval.lower + math.ceil((interval.upper - interval.lower) / 2),
            interval.upper,
        )
    raise Exception(f"invalid BSP operation {oper}")


def parse_row(input: str) -> int:
    interval = Interval(0, 127)
    for c in input[:7]:
        interval = apply_bsp_oper(c, interval)
    assert interval.lower == interval.upper
    return interval.lower


def parse_column(input: str) -> int:
    interval = Interval(0, 7)
    for c in input[7:]:
        interval = apply_bsp_oper(c, interval)
    assert interval.lower == interval.upper
    return interval.lower


def get_seat_id(seat: Seat) -> int:
    return seat.row * 8 + seat.column


def get_my_seat(seats: Iterable[Seat]) -> int:
    sorted_seats = sorted(map(get_seat_id, seats))
    current_seat = sorted_seats[0]
    for s in sorted_seats[1:]:
        if s == current_seat + 2:
            return s - 1
        current_seat = s
    raise Exception("seat not found")


if __name__ == "__main__":
    debug = "--debug" in sys.argv
    seats = parse_input(sys.argv[-1])

    print(f"answer: {get_my_seat(seats)}")
