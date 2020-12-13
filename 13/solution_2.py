#!/usr/bin/env python

import sys
from typing import IO, Any, List, Optional, Tuple

debug: bool = False
logfile: Optional[IO[Any]] = None


def log(msg: str) -> None:
    global logfile
    if debug:
        if logfile is None:
            logfile = open("output", "w")
        logfile.write(msg + "\n")


def parse_line(line: str) -> List[Tuple[int, int]]:
    buses = []
    for offset, bus in enumerate(line.split(",")):
        if bus == "x":
            continue
        buses.append((offset, int(bus)))
    return buses


def parse_input(filename: str) -> List[Tuple[int, int]]:
    with open(filename, "r") as f:
        f.readline()  # ignore first line
        return parse_line(f.readline().strip())


def valid_timestamp(time: int, buses: List[Tuple[int, int]]) -> bool:
    for offset, bus in buses:
        if (time + offset) % bus != 0:
            return False
    return True


def find_valid_timestamp(buses: List[Tuple[int, int]]) -> int:
    first_bus_time = buses[0][1]
    time = first_bus_time
    while not valid_timestamp(time, buses):
        time += first_bus_time
        print(f"{time}")
    return time


if __name__ == "__main__":
    debug = "--debug" in sys.argv
    buses = parse_input(sys.argv[-1])

    answer = find_valid_timestamp(buses)

    print(f"answer: {answer}")
