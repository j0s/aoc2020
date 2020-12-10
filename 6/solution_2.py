#!/usr/bin/env python

import sys
from typing import IO, Any, Optional, Iterable, Set, List
from functools import reduce

debug: bool = False
logfile: Optional[IO[Any]] = None


def log(msg: str) -> None:
    global logfile
    if debug:
        if logfile is None:
            logfile = open("output", "w")
        logfile.write(msg + "\n")


def parse_input(filename: str) -> Iterable[Set[str]]:
    with open(filename, "r") as f:
        group_choices: List[Set[str]] = []
        for line in f:
            line = line.strip()
            if line == "":
                log(f"yielding {group_choices}")
                yield reduce(lambda x, y: x.intersection(y), group_choices)
                group_choices = []
                continue
            group_choices.append(set(line))
        log(f"yielding {group_choices}")
        yield reduce(lambda x, y: x.intersection(y), group_choices)


if __name__ == "__main__":
    debug = "--debug" in sys.argv
    group_choices = parse_input(sys.argv[-1])
    num_choices = [len(choices) for choices in group_choices]

    print(f"answer: {sum(num_choices)}")
