#!/usr/bin/env python

import sys
from typing import IO, Any, List, Optional, Dict, Tuple, Callable
from enum import Enum
from dataclasses import dataclass

debug: bool = False
logfile: Optional[IO[Any]] = None


class Direction(Enum):
    NORTH = 0
    EAST = 90
    SOUTH = 180
    WEST = 270


@dataclass
class Ship:
    x: int
    y: int
    direction: Direction


def log(msg: str) -> None:
    global logfile
    if debug:
        if logfile is None:
            logfile = open("output", "w")
        logfile.write(msg + "\n")


def turn_left(ship: Ship, arg: int) -> None:
    ship.direction = Direction((ship.direction.value - arg) % 360)


def turn_right(ship: Ship, arg: int) -> None:
    ship.direction = Direction((ship.direction.value + arg) % 360)


def move(ship: Ship, direction: Direction, arg: int) -> None:
    if direction == Direction.NORTH:
        ship.y += arg
    elif direction == Direction.SOUTH:
        ship.y -= arg
    elif direction == Direction.EAST:
        ship.x += arg
    elif direction == Direction.WEST:
        ship.x -= arg


def go_forward() -> Callable[[Ship, int], None]:
    return lambda ship, arg: move(ship, ship.direction, arg)


def go_direction(dir: Direction) -> Callable[[Ship, int], None]:
    return lambda ship, arg: move(ship, dir, arg)


movements: Dict[str, Callable[[Ship, int], None]] = {
    "L": turn_left,
    "R": turn_right,
    "F": go_forward(),
    "N": go_direction(Direction.NORTH),
    "S": go_direction(Direction.SOUTH),
    "E": go_direction(Direction.EAST),
    "W": go_direction(Direction.WEST),
}


def parse_input(filename: str) -> List[Tuple[str, int]]:
    with open(filename, "r") as f:
        commends = []
        for line in f:
            line = line.strip()
            commends.append((line[0], int(line[1:])))
        return commends


def apply_movement(ship: Ship, movement: Tuple[str, int]):
    cmd, arg = movement
    movements[cmd](ship, arg)
    print(f"applied {cmd} {arg} to {ship}")


if __name__ == "__main__":
    debug = "--debug" in sys.argv
    ship = Ship(0, 0, Direction.EAST)
    commands = parse_input(sys.argv[-1])
    for cmd in commands:
        apply_movement(ship, cmd)

    print(f"ship: {ship}, dist: {abs(ship.y) + abs(ship.x)}")
