#!/usr/bin/env python

import sys
from typing import IO, Any, Optional, Iterable, Dict, List

debug: bool = False
logfile: Optional[IO[Any]] = None


def log(msg: str) -> None:
    global logfile
    if debug:
        if logfile is None:
            logfile = open("output", "w")
        logfile.write(msg + "\n")


def parse_input(filename: str) -> Iterable[int]:
    with open(filename, "r") as f:
        for line in f:
            for n in line.strip().split(","):
                yield int(n)


def get_sequence(start_numbers: Iterable[int], length: int) -> List[int]:
    visited_numbers: Dict[int, List[int]] = {}
    sequence = []
    for round, n in enumerate(start_numbers):
        visited_numbers[n] = [round]
        sequence.append(n)
    while (round := round + 1) < length:
        last_n = sequence[-1]
        last_n_rounds = visited_numbers[last_n]
        this_n = 0 if len(last_n_rounds) == 1 else (round - 1 - last_n_rounds[-2])
        this_n_rounds = visited_numbers.setdefault(this_n, [])
        if len(this_n_rounds) > 2:
            this_n_rounds = this_n_rounds[-1:]
        this_n_rounds.append(round)
        visited_numbers[this_n] = this_n_rounds
        sequence.append(this_n)
        if round % 10000 == 0:
            print(round)

    return sequence


def get_last_number(start_numbers: Iterable[int], length: int) -> int:
    return get_sequence(start_numbers, length)[-1]


if __name__ == "__main__":
    debug = "--debug" in sys.argv
    start_numbers = parse_input(sys.argv[-1])
    sequence = get_sequence(start_numbers, 30000000)

    print(f"answer: {sequence[-1]}")
