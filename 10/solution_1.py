#!/usr/bin/env python

import sys
from typing import IO, Any, List, Optional, Dict

debug: bool = False
logfile: Optional[IO[Any]] = None


def log(msg: str) -> None:
    global logfile
    if debug:
        if logfile is None:
            logfile = open("output", "w")
        logfile.write(msg + "\n")


def get_jolt_differences(jolts: List[int]) -> Dict[int, int]:
    jolts.sort()
    jolts.append(jolts[-1] + 3)
    last = 0
    differences: Dict[int, int] = {}
    for j in jolts:
        differences.setdefault(j - last, 0)
        differences[j - last] += 1
        last = j
    return differences


def parse_input(filename: str) -> List[int]:
    with open(filename, "r") as f:
        return [int(line.strip()) for line in f]


if __name__ == "__main__":
    debug = "--debug" in sys.argv
    jolts = parse_input(sys.argv[-1])
    differences = get_jolt_differences(jolts)
    print(f"differences: {differences}, answer: {differences[1] * differences[3]}")
