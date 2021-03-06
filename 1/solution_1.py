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


def parse_input(filename: str) -> List[int]:
    nums: List[int] = []
    with open(filename, 'r') as f:
        for line in f:
            nums.append(int(line))
    return nums


def find_numbers_totalling(numbers: List[int], pair_sum: int) -> Tuple[int, int]:
    for i1, n1 in enumerate(numbers):
        if n1 > pair_sum:
            continue
        for n2 in numbers[i1+1:]:
            if n1 + n2 == pair_sum:
                return (n1, n2)

    raise BaseException("Not found")


if __name__ == '__main__':
    debug = '--debug' in sys.argv
    numbers = parse_input('input')
    n1, n2 = find_numbers_totalling(numbers, 2020)

    print(f'n1: {n1}, n2: {n2}, sum: {n1 + n2}, product: {n1 * n2}')
