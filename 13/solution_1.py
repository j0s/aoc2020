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


def parse_input(filename: str) -> Tuple[int, List[int]]:
    with open(filename, "r") as f:
        earliest_time = int(f.readline().strip())
        buses = [int(n) for n in f.readline().strip().split(",") if n != "x"]
        return (earliest_time, buses)


def get_waiting_time(bus: int, time: int) -> int:
    return bus - (time % bus)


if __name__ == "__main__":
    debug = "--debug" in sys.argv
    time, buses = parse_input(sys.argv[-1])
    waiting_times = [(bus, get_waiting_time(bus, time)) for bus in buses]

    best_bus, waiting_time = min(waiting_times, key=lambda x: x[1])
    print(
        f"best bus: {best_bus}, waiting time: {waiting_time}, "
        f"answer: {best_bus * waiting_time}"
    )
