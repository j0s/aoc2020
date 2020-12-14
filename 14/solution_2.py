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
    floating: List[int] = field(default_factory=list)
    memory: Dict[int, int] = field(default_factory=dict)


def parse_input(filename: str) -> Iterable[List[str]]:
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            yield line.split()


def parse_mask(mask: str) -> Tuple[int, List[int]]:
    pos, floating = 0, []
    for i, char in enumerate(reversed(mask)):
        if char == "1":
            pos += 2 ** i
        elif char == "X":
            floating.append(i)

    return pos, floating


def set_bit(number: int, bit: int, value: bool) -> int:
    if value is True:
        return number | (2 ** bit)
    else:
        return number & (2 ** 36 - 1 - 2 ** bit)


def generate_addresses(original_addr: int, floating_pos: List[int]) -> List[int]:
    if len(floating_pos) == 0:
        return [original_addr]

    floating_pos_false = set_bit(original_addr, floating_pos[0], False)
    floating_pos_true = set_bit(original_addr, floating_pos[0], True)
    return [
        *generate_addresses(floating_pos_false, floating_pos[1:]),
        *generate_addresses(floating_pos_true, floating_pos[1:]),
    ]


def run_program(commands: Iterable[List[str]]) -> State:
    state = State()
    for tokens in commands:
        if tokens[0] == "mask":
            (
                state.positive_mask,
                state.floating,
            ) = parse_mask(tokens[2])
        else:  # "mem"
            initial_addr = int(tokens[0][4:-1]) | state.positive_mask
            value = int(tokens[2])
            for addr in generate_addresses(initial_addr, state.floating):
                state.memory[addr] = value
    return state


if __name__ == "__main__":
    debug = "--debug" in sys.argv
    commands = parse_input(sys.argv[-1])
    state = run_program(commands)

    print(f"answer: {sum(state.memory.values())}")
