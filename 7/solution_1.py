#!/usr/bin/env python

import sys
from typing import IO, Any, Set, Dict, List, Optional
from functools import reduce
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
class ColorSpec:
    num: int
    color: BagColor


def parse_content_string(content_str: str) -> List[ColorSpec]:
    if content_str == "no other bags.":
        return []
    color_specs = []
    color_spec_strs = content_str.split(",")
    for color_spec in color_spec_strs:
        tokens = color_spec.split()
        color_specs.append(ColorSpec(int(tokens[0]), f"{tokens[1]} {tokens[2]}"))
    return color_specs


def parse_input(filename: str) -> Dict[BagColor, Set[BagColor]]:
    can_be_in: Dict[BagColor, Set[BagColor]] = {}
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            parent_color, contents_list = line.split(" bags contain ")
            child_color_specs = parse_content_string(contents_list)
            for child_color_spec in child_color_specs:
                can_be_in.setdefault(child_color_spec.color, set())
                can_be_in[child_color_spec.color].add(parent_color)
    return can_be_in


def get_valid_containers(
    can_be_in: Dict[BagColor, Set[BagColor]], color: BagColor
) -> Set[BagColor]:
    valid_containers = can_be_in.setdefault(color, set())
    return reduce(
        lambda x, y: (get_valid_containers(can_be_in, y) | x),
        valid_containers,
        valid_containers,
    )


if __name__ == "__main__":
    debug = "--debug" in sys.argv
    color = parse_input(sys.argv[-1])
    print(len(get_valid_containers(color, "shiny gold")))
