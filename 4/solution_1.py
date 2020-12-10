#!/usr/bin/env python

import sys
from typing import IO, Any, Optional, Set, Iterable
from dataclasses import dataclass, field

debug: bool = False
logfile: Optional[IO[Any]] = None


def log(msg: str) -> None:
    global logfile
    if debug:
        if logfile is None:
            logfile = open("output", "w")
        logfile.write(msg + "\n")


required_fields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}


@dataclass
class Passport:
    fields: Set[str] = field(default_factory=set)


def parse_input(filename: str) -> Iterable[Passport]:
    with open(filename, "r") as f:
        passport = Passport()
        for line in f:
            line = line.strip()
            if line == "":
                log(f"pass: {passport}")
                yield passport
                passport = Passport()
            for token in line.split(" "):
                if token.strip() == "":
                    continue
                _field, _ = token.split(":")
                passport.fields.add(_field)
        log(f"pass: {passport}")
        yield passport


def validate_passport(passport: Passport) -> bool:
    log(
        f"is {passport.fields} a superset of {required_fields}? {passport.fields.issuperset(required_fields)}"
    )
    return passport.fields.issuperset(required_fields)


if __name__ == "__main__":
    debug = "--debug" in sys.argv
    passports = parse_input(sys.argv[-1])
    valid_passports = filter(validate_passport, passports)

    print(f"valid passports: {len(list(valid_passports))}")
