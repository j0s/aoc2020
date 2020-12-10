#!/usr/bin/env python

import sys
from typing import IO, Any, List, Optional
from dataclasses import dataclass

debug: bool = False
logfile: Optional[IO[Any]] = None


def log(msg: str) -> None:
    global logfile
    if debug:
        if logfile is None:
            logfile = open("output", "w")
        logfile.write(msg + "\n")


BagColor = str


@dataclass
class Operation:
    oper: str
    arg: int


def validate_number(preamble: List[int], number: int) -> bool:
    sorted_preamble = preamble[:]
    sorted_preamble.sort()
    for i, n in enumerate(sorted_preamble):
        if n >= number / 2:
            return False
        if number - n in sorted_preamble[i:]:
            return True
    return False


def find_invalid_data(data: List[int], preamble_size: int) -> Optional[int]:
    while len(data) > preamble_size:
        if not validate_number(data[:preamble_size], data[preamble_size]):
            return data[preamble_size]
        data.pop(0)
    return None


def parse_input(filename: str) -> List[int]:
    with open(filename, "r") as f:
        return [int(line.strip()) for line in f]


if __name__ == "__main__":
    debug = "--debug" in sys.argv
    program = parse_input(sys.argv[-2])
    preamble_size = int(sys.argv[-1])
    print(find_invalid_data(program, preamble_size))
