#!/usr/bin/env python

import sys
import re
from typing import IO, Any, Optional, List, Tuple, Dict, Set
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


@dataclass
class Constraint:
    name: str
    ranges: Tuple[range, range]


Ticket = List[int]


def parse_input(filename: str) -> Tuple[List[Constraint], Ticket, List[Ticket]]:
    with open(filename, "r") as f:
        constraints: List[Constraint] = []
        my_ticket: Ticket = []
        nearby_tickets: List[Ticket] = []
        section = "constraints"
        for line in f:
            line = line.strip()
            if line in ["your ticket:", "nearby tickets:"]:
                section = line[:-1]
                continue
            elif line == "":
                continue

            if section == "constraints":
                match = re.match(r"([^:]+): (\d+)-(\d+) or (\d+)-(\d+)", line)
                assert match is not None
                c = Constraint(
                    match.group(1),
                    (
                        range(int(match.group(2)), int(match.group(3)) + 1),
                        range(int(match.group(4)), int(match.group(5)) + 1),
                    ),
                )
                constraints.append(c)
            elif section == "your ticket":
                my_ticket = [int(t) for t in line.split(",")]
            elif section == "nearby tickets":
                nearby_tickets.append([int(t) for t in line.split(",")])
        return constraints, my_ticket, nearby_tickets


def completely_invalid_field(constraints: List[Constraint], value: int) -> bool:
    for constraint in constraints:
        if value in constraint.ranges[0] or value in constraint.ranges[1]:
            return False
    return True


def completely_invalid_ticket(constraints: List[Constraint], ticket: Ticket) -> bool:
    for field in ticket:
        if completely_invalid_field(constraints, field):
            return True
    return False


def complies(constraint: Constraint, value: int) -> bool:
    return value in constraint.ranges[0] or value in constraint.ranges[1]


def get_field_mapping(
    constraints: List[Constraint], nearby_tickets: List[Ticket]
) -> Dict[str, Set[int]]:
    nearby_tickets = list(
        filter(lambda t: not completely_invalid_ticket(constraints, t), nearby_tickets)
    )
    num_fields = len(nearby_tickets[0])
    field_candidates = {
        constraint.name: set(range(num_fields)) for constraint in constraints
    }
    for ticket in nearby_tickets:
        for index, value in enumerate(ticket):
            for c in constraints:
                if not complies(c, value):
                    field_candidates[c.name].discard(index)

    return field_candidates


def reduce_candidates(candidates: Dict[str, Set[int]]) -> Dict[str, int]:
    result: Dict[str, int] = {}
    taken: Set[int] = set()
    while len(result) < len(candidates):
        for name, alternatives in candidates.items():
            alternatives -= taken
            if len(alternatives) == 1:
                result[name] = alternatives.pop()
                taken.add(result[name])
    return result


if __name__ == "__main__":
    debug = "--debug" in sys.argv
    constraints, my_ticket, nearby_tickets = parse_input(sys.argv[-1])
    mapping_candidates = get_field_mapping(constraints, nearby_tickets)
    mapping = reduce_candidates(mapping_candidates)

    answer = reduce(
        lambda x, y: x * y,
        [my_ticket[i] for n, i in mapping.items() if n.startswith("departure")],
    )

    print(f"answer: {answer}")
