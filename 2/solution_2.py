#!/usr/bin/env python

import sys
from typing import List, Tuple, IO, Any, Optional

debug: bool = False
logfile: Optional[IO[Any]] = None


def log(msg: str) -> None:
    global logfile
    if debug:
        if logfile is None:
            logfile = open('output', 'w')
        logfile.write(msg+'\n')


def parse_input(filename: str) -> List[Tuple[int, int, str, str]]:
    rules: List[Tuple[int, int, str, str]] = []
    with open(filename, 'r') as f:
        for line in f:
            tokens = line.split(' ')
            rule_min, rule_max = map(int, tokens[0].split('-'))
            char = tokens[1].strip(':')
            passwd = tokens[2]
            rules.append((rule_min, rule_max, char, passwd))
    return rules


def find_valid_passwords(numbers: List[Tuple[int, int, str, str]]) -> int:
    valid_passwds: int = 0
    for rule_min, rule_max, char, passwd in numbers:
        valid_passwds += \
            (passwd[rule_min-1] == char) ^ (passwd[rule_max-1] == char)
    return valid_passwds


if __name__ == '__main__':
    debug = '--debug' in sys.argv
    numbers = parse_input(sys.argv[-1])
    valid_passwords = find_valid_passwords(numbers)

    print(f'valid passwords: {valid_passwords}')
