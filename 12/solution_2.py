#!/usr/bin/env python

import sys
from typing import IO, Any, List, Optional, Dict, Tuple, Callable
from dataclasses import dataclass

debug: bool = False
logfile: Optional[IO[Any]] = None


@dataclass
class Ship:
    x: int
    y: int
    wp_x_relative: int
    wp_y_relative: int


def log(msg: str) -> None:
    global logfile
    if debug:
        if logfile is None:
            logfile = open("output", "w")
        logfile.write(msg + "\n")


def rotate_wp_left(ship: Ship, arg: int) -> None:
    for _ in range(int(arg / 90)):
        ship.wp_x_relative, ship.wp_y_relative = (
            -ship.wp_y_relative,
            ship.wp_x_relative,
        )


def rotate_wp_right(ship: Ship, arg: int) -> None:
    for _ in range(int(arg / 90)):
        ship.wp_x_relative, ship.wp_y_relative = (
            ship.wp_y_relative,
            -ship.wp_x_relative,
        )


def move_ship(ship: Ship, arg: int) -> None:
    ship.x += arg * ship.wp_x_relative
    ship.y += arg * ship.wp_y_relative


def move_wp(x: int, y) -> Callable[[Ship, int], None]:
    def move(ship: Ship, arg: int):
        ship.wp_x_relative += x * arg
        ship.wp_y_relative += y * arg

    return move


movements: Dict[str, Callable[[Ship, int], None]] = {
    "L": rotate_wp_left,
    "R": rotate_wp_right,
    "F": move_ship,
    "N": move_wp(0, 1),
    "S": move_wp(0, -1),
    "E": move_wp(1, 0),
    "W": move_wp(-1, 0),
}


def parse_input(filename: str) -> List[Tuple[str, int]]:
    with open(filename, "r") as f:
        commands = []
        for line in f:
            line = line.strip()
            commands.append((line[0], int(line[1:])))
        return commands


def apply_movement(ship: Ship, movement: Tuple[str, int]):
    cmd, arg = movement
    movements[cmd](ship, arg)
    print(f"applied {cmd} {arg} to {ship}")


if __name__ == "__main__":
    debug = "--debug" in sys.argv
    ship = Ship(0, 0, 10, 1)
    commands = parse_input(sys.argv[-1])
    for cmd in commands:
        apply_movement(ship, cmd)

    print(f"ship: {ship}, dist: {abs(ship.y) + abs(ship.x)}")
