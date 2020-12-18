#!/usr/bin/env python

import sys
import re
from typing import IO, Any, Optional, List

debug: bool = False
logfile: Optional[IO[Any]] = None


def log(msg: str) -> None:
    global logfile
    if debug:
        if logfile is None:
            logfile = open("output", "w")
        logfile.write(msg + "\n")


oper_mapping = {
    "+": lambda x, y: x + y,
    "*": lambda x, y: x * y,
}


def eval_expr_str(expr: str) -> int:
    tokens = re.split(r"( |\(|\))", expr)
    tokens.reverse()
    tokens = list(filter(lambda x: x != " " and x != "", tokens))
    return eval_expr(tokens)


def eval_expr(expr: List[str]) -> int:
    if len(expr) == 1:
        return int(expr[0])
    lhs: Optional[int] = None
    print(expr)
    for i, token in enumerate(expr):
        if token in oper_mapping:
            assert lhs is not None
            start_ix = i + 1
            rhs = eval_expr(expr[start_ix:])
            oper = token
            res = oper_mapping[oper](lhs, rhs)
            print(lhs, oper, rhs, "=", res)
            return res
        elif token == ")":
            end_ix = expr.index("(")
            lhs = eval_expr(expr[1:end_ix])
            print("lhs", lhs)
            end_ix += 1
            del expr[1:end_ix]
        elif token == "(":
            assert False
        else:
            lhs = int(token)
    assert lhs is not None
    return lhs


def parse_input(filename: str) -> int:
    results = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            results.append(eval_expr_str(line))

        return sum(results)


if __name__ == "__main__":
    debug = "--debug" in sys.argv
    answer = parse_input(sys.argv[-1])

    print(f"answer: {answer}")
