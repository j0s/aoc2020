#!/usr/bin/env python

import sys
from typing import IO, Any, List, Optional, Dict, Iterable, Tuple
from dataclasses import dataclass, field

debug: bool = False
logfile: Optional[IO[Any]] = None


def log(msg: str) -> None:
    global logfile
    if debug:
        if logfile is None:
            logfile = open("output", "w")
        logfile.write(msg + "\n")


@dataclass
class State:
    positive_mask: int = 0
    negative_mask: int = 0
    memory: Dict[int, int] = field(default_factory=dict)


def parse_input(filename: str) -> Iterable[List[str]]:
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            yield line.split()


def parse_mask(mask: str) -> Tuple[int, int]:
    pos, neg = 0, 2 ** 36 - 1
    for i, char in enumerate(reversed(mask)):
        if char == "1":
            pos += 2 ** i
        elif char == "0":
            neg -= 2 ** i
    return pos, neg


def run_program(commands: Iterable[List[str]]) -> State:
    state = State()
    for tokens in commands:
        if tokens[0] == "mask":
            state.positive_mask, state.negative_mask = parse_mask(tokens[2])
        else:  # "mem"
            addr = int(tokens[0][4:-1])
            value = int(tokens[2])
            state.memory[addr] = (value | state.positive_mask) & state.negative_mask
    return state


if __name__ == "__main__":
    debug = "--debug" in sys.argv
    commands = parse_input(sys.argv[-1])
    state = run_program(commands)

    print(f"answer: {sum(state.memory.values())}")
