#!/usr/bin/env python

import sys
from typing import IO, Any, Dict, List, Optional
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


@dataclass(frozen=True)
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


def parse_input(filename: str) -> Dict[BagColor, List[ColorSpec]]:
    contains: Dict[BagColor, List[ColorSpec]] = {}
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            parent_color, contents_list = line.split(" bags contain ")
            contains.setdefault(parent_color, [])
            child_color_specs = parse_content_string(contents_list)
            for child_color_spec in child_color_specs:
                contains[parent_color].append(child_color_spec)
    return contains


def get_bag_contents(
    contains: Dict[BagColor, List[ColorSpec]], color: ColorSpec
) -> List[ColorSpec]:
    children = contains.setdefault(color.color, [])
    children = list(map(lambda c: ColorSpec(c.num * color.num, c.color), children))
    return reduce(
        lambda x, y: get_bag_contents(contains, y) + x,
        children,
        list(children),
    )


if __name__ == "__main__":
    debug = "--debug" in sys.argv
    color = parse_input(sys.argv[-1])
    bag_contents = get_bag_contents(color, ColorSpec(1, "shiny gold"))
    print(reduce(lambda x, y: x + y.num, bag_contents, 0))
