#!/usr/bin/env python

import sys
from typing import IO, Any, Optional, Iterable, Set

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
        choices: Set[str] = set()
        for line in f:
            line = line.strip()
            if line == "":
                yield choices
                choices = set()
            for char in line:
                choices.add(char)
        yield choices


if __name__ == "__main__":
    debug = "--debug" in sys.argv
    group_choices = parse_input(sys.argv[-1])
    num_choices = [len(choices) for choices in group_choices]

    print(f"answer: {num_choices} {sum(num_choices)}")
