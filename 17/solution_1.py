#!/usr/bin/env python

import sys
from typing import IO, Any, Optional, Set
from dataclasses import dataclass

debug: bool = False
logfile: Optional[IO[Any]] = None


def log(msg: str) -> None:
    global logfile
    if debug:
        if logfile is None:
            logfile = open("output", "w")
        logfile.write(msg + "\n")


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int


def parse_input(filename: str) -> Set[Point]:
    pocket = set()
    with open(filename, "r") as f:
        for y, line in enumerate(f):
            line = line.strip()
            for x, char in enumerate(line):
                if char == "#":
                    pocket.add(Point(x, y, 0))

        return pocket


def calc_next_status(point: Point, pocket: Set[Point]) -> bool:
    active_neighbors = 0
    active = point in pocket
    for x in range(point.x - 1, point.x + 2):
        for y in range(point.y - 1, point.y + 2):
            for z in range(point.z - 1, point.z + 2):
                if (point.x, point.y, point.z) == (x, y, z):
                    continue
                if Point(x, y, z) in pocket:
                    active_neighbors += 1
    if active:
        return 2 <= active_neighbors <= 3
    if not active:
        return active_neighbors == 3

    return active


def simulate(pocket: Set[Point]) -> Set[Point]:
    max_x = max([point.x for point in pocket])
    min_x = min([point.x for point in pocket])
    max_y = max([point.y for point in pocket])
    min_y = min([point.y for point in pocket])
    max_z = max([point.z for point in pocket])
    min_z = min([point.z for point in pocket])

    next_pocket = set()
    for z in range(min_z - 1, max_z + 2):
        log(f"{z}:")
        for y in range(min_y - 1, max_y + 2):
            line = ""
            for x in range(min_x - 1, max_x + 2):
                point = Point(x, y, z)
                if calc_next_status(point, pocket):
                    line += "#"
                    next_pocket.add(point)
                else:
                    line += "."
            log(line)
    return next_pocket


if __name__ == "__main__":
    debug = "--debug" in sys.argv
    pocket = parse_input(sys.argv[-1])
    print(pocket)

    for _ in range(6):
        pocket = simulate(pocket)

    print(f"answer: {len(pocket)}")
