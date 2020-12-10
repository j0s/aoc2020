#!/usr/bin/env python

import sys
from typing import IO, Any, Optional, Set
from dataclasses import dataclass, field

debug: bool = False
logfile: Optional[IO[Any]] = None


def log(msg: str) -> None:
    global logfile
    if debug:
        if logfile is None:
            logfile = open("output", "w")
        logfile.write(msg + "\n")


@dataclass(frozen=True)
class Coord:
    x: int
    y: int


@dataclass
class Layout:
    Width: int = 0
    TreeIndices: Set[Coord] = field(default_factory=set)


def parse_input(filename: str) -> Layout:
    layout = Layout()
    with open(filename, "r") as f:
        for y, line in enumerate(f):
            line = line.strip()
            if layout.Width == 0:
                layout.Width = len(line)
                log(f"width: {layout.Width}")
            for x, token in enumerate(line):
                if token == "#":
                    log(f"tree@({x}, {y})")
                    layout.TreeIndices.add(Coord(x, y))
    return layout


@dataclass
class Slope:
    down: int
    right: int


def encountered_trees(slope: Slope, layout: Layout) -> int:
    x, y = 0, 0
    trees = 0
    while y < len(layout.TreeIndices):
        x += slope.right
        y += slope.down
        log(f"checking {x} ({x % layout.Width}), {y}")
        if Coord(x % layout.Width, y) in layout.TreeIndices:
            log(f"hit! {x % layout.Width}, {y}")
            trees += 1
    return trees


if __name__ == "__main__":
    debug = "--debug" in sys.argv
    forest = parse_input(sys.argv[-1])
    num_trees = encountered_trees(Slope(down=1, right=3), forest)

    print(f"trees hit: {num_trees}")
