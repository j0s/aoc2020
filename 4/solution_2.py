#!/usr/bin/env python

import sys
from typing import IO, Any, Optional, Dict, Iterable, Callable
from dataclasses import dataclass, field

debug: bool = False
logfile: Optional[IO[Any]] = None


def log(msg: str) -> None:
    global logfile
    if debug:
        if logfile is None:
            logfile = open("output", "w")
        logfile.write(msg + "\n")


def validate_hcl(hcl: str) -> bool:
    if hcl[0] != "#" or len(hcl) != 7:
        return False
    for c in hcl[1:]:
        if c < "0" or "9" < c < "a" or c > "f":
            return False
    return True


Validator = Callable[[str], bool]

required_fields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
validators: Dict[str, Validator] = {
    "byr": lambda x: 1920 <= int(x) <= 2002,
    "iyr": lambda x: 2010 <= int(x) <= 2020,
    "eyr": lambda x: 2020 <= int(x) <= 2030,
    "hgt": lambda x: (
        (x.endswith("cm") and 150 <= int(x[:-2]) <= 193)
        or (x.endswith("in") and 59 <= int(x[:-2]) <= 76)
    ),
    "hcl": validate_hcl,
    "ecl": lambda x: x in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"},
    "pid": lambda x: len(x) == 9 and x.isdecimal(),
}


@dataclass
class Passport:
    fields: Dict[str, str] = field(default_factory=dict)


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
                _field, val = token.split(":")
                passport.fields[_field] = val
        log(f"pass: {passport}")
        yield passport


def validate_passport(passport: Passport) -> bool:
    for key, val in passport.fields.items():
        if key in validators and not validators[key](val):
            return False
    return set(passport.fields.keys()).issuperset(required_fields)


if __name__ == "__main__":
    debug = "--debug" in sys.argv
    passports = parse_input(sys.argv[-1])
    valid_passports = filter(validate_passport, passports)

    print(f"valid passports: {len(list(valid_passports))}")
