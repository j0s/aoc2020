#!/usr/bin/env python

import sys
from typing import IO, Any, List, Tuple, Optional
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


def find_invalid_data(_data: List[int], preamble_size: int) -> Optional[int]:
    data = _data[:]
    while len(data) > preamble_size:
        if not validate_number(data[:preamble_size], data[preamble_size]):
            return data[preamble_size]
        data.pop(0)
    return None


def find_components_sequence(data: List[int], number: int) -> Optional[Tuple[int, int]]:
    _from = 0
    to = 0
    comp_sum = 0
    while to < len(data):
        if comp_sum < number:
            comp_sum += data[to]
            to += 1
            log(f"{_from}, {to}: {comp_sum}")
        elif comp_sum > number:
            comp_sum -= data[_from]
            _from += 1
            log(f"{_from}, {to}: {comp_sum}")
        elif comp_sum == number:
            seq = data[_from:to]
            return min(seq), max(seq)
        if _from >= to:
            log(f"{_from}, {to}")
            log(f"{data[_from]}, {data[to]}")
            return None
    return None


def parse_input(filename: str) -> List[int]:
    with open(filename, "r") as f:
        return [int(line.strip()) for line in f]


if __name__ == "__main__":
    debug = "--debug" in sys.argv
    program = parse_input(sys.argv[-2])
    preamble_size = int(sys.argv[-1])
    invalid_no = find_invalid_data(program, preamble_size)
    if invalid_no is None:
        print("no invalid number found")
    else:
        seq = find_components_sequence(program, invalid_no)
        if seq is None:
            print("no sequence found")
        else:
            print(f"{seq[0]} {seq[1]}: {seq[0]+seq[1]}")
