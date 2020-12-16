#!/usr/bin/env python

import sys
import re
from typing import IO, Any, Optional, List, Tuple

debug: bool = False
logfile: Optional[IO[Any]] = None


def log(msg: str) -> None:
    global logfile
    if debug:
        if logfile is None:
            logfile = open("output", "w")
        logfile.write(msg + "\n")


Constraints = List[range]
Ticket = List[int]


def parse_input(filename: str) -> Tuple[Constraints, Ticket, List[Ticket]]:
    with open(filename, "r") as f:
        constraints: Constraints = []
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
                constraints.append(range(int(match.group(2)), int(match.group(3)) + 1))
                constraints.append(range(int(match.group(4)), int(match.group(5)) + 1))
            elif section == "your ticket":
                pass
            elif section == "nearby tickets":
                nearby_tickets.append([int(t) for t in line.split(",")])
        return constraints, my_ticket, nearby_tickets


def completely_invalid(constraints: Constraints, value: int) -> bool:
    for constraint in constraints:
        if value in constraint:
            return False
    return True


def scanning_error_rate(constraints: Constraints, nearby_tickets: List[Ticket]) -> int:
    completely_invalid_fields = []
    print(constraints)
    for ticket in nearby_tickets:
        for field in ticket:
            if completely_invalid(constraints, field):
                print(field)
                completely_invalid_fields.append(field)
    return sum(completely_invalid_fields)


if __name__ == "__main__":
    debug = "--debug" in sys.argv
    constraints, _, nearby_tickets = parse_input(sys.argv[-1])
    answer = scanning_error_rate(constraints, nearby_tickets)

    print(f"answer: {answer}")
