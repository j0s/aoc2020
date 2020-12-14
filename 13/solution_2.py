#!/usr/bin/env python

import sys
from typing import IO, Any, List, Optional, Tuple
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
class Bus:
    time: int
    offset: int


def parse_line(line: str) -> List[Bus]:
    buses = []
    for offset, time in enumerate(line.split(",")):
        if time == "x":
            continue
        buses.append(Bus(int(time), offset))
    return buses


def parse_input(filename: str) -> List[Bus]:
    with open(filename, "r") as f:
        f.readline()  # ignore first line
        return parse_line(f.readline().strip())


def lcd(a: int, b: int) -> int:
    if b == 0:
        return a
    return lcd(b, a % b)


def lcm(a: int, b: int) -> int:
    x = a // lcd(a, b) * b
    return x


def solve_two(bus: Bus, start_time: int, min_increase: int) -> Tuple[int, int]:
    while (start_time + bus.offset) % bus.time != 0:
        start_time += min_increase
    return start_time, lcm(bus.time, min_increase)


def find_valid_timestamp(buses: List[Bus]) -> int:
    start_time = min_increase = buses[0].time
    for bus in buses:
        start_time, min_increase = solve_two(bus, start_time, min_increase)
        print(bus, start_time, min_increase)

    for bus in buses:
        assert (start_time + bus.offset) % bus.time == 0

    return start_time


if __name__ == "__main__":
    debug = "--debug" in sys.argv
    buses = parse_input(sys.argv[-1])

    answer = find_valid_timestamp(buses)

    print(f"answer: {answer}")
