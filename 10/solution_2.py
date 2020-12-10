#!/usr/bin/env python

import sys
from typing import IO, Any, List, Optional, Dict

debug: bool = False
logfile: Optional[IO[Any]] = None


def log(msg: Any) -> None:
    global logfile
    if debug:
        if logfile is None:
            logfile = open("output", "w")
        logfile.write(f"{msg}\n")


def get_jolt_permutations(jolts: List[int]) -> int:
    jolts.sort()
    jolts.reverse()
    jolts.append(0)
    permutations: Dict[int, int] = {jolts[0]: 1}
    for jolt in jolts[1:]:
        permutations[jolt] = sum(
            [permutations.get(jolt + offset, 0) for offset in range(1, 4)]
        )
    log(permutations)

    return permutations[0]


def parse_input(filename: str) -> List[int]:
    with open(filename, "r") as f:
        return [int(line.strip()) for line in f]


if __name__ == "__main__":
    debug = "--debug" in sys.argv
    jolts = parse_input(sys.argv[-1])
    permutations = get_jolt_permutations(jolts)
    print(f"answer: {permutations}")
