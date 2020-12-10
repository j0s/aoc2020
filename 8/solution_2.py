#!/usr/bin/env python

import sys
from typing import IO, Any, List, Optional
from dataclasses import dataclass

debug: bool = False
logfile: Optional[IO[Any]] = None


def log(msg: str) -> None:
    global logfile
    if debug:
        if logfile is None:
            logfile = open("output", "w")
        logfile.write(msg + "\n")


BagColor = str


@dataclass
class Operation:
    oper: str
    arg: int


def parse_input(filename: str) -> List[Operation]:
    program: List[Operation] = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            oper, arg_str = line.split()
            program.append(Operation(oper, int(arg_str)))

    return program


def run_program(program: List[Operation]):
    acc = 0
    pc = 0
    used_pc_values = set()
    while pc not in used_pc_values and pc < len(program):
        op = program[pc]
        used_pc_values.add(pc)
        log(f"{op.oper} {op.arg} (acc: {acc}, pc: {pc})")
        if op.oper == "acc":
            acc += op.arg
            pc += 1
        elif op.oper == "jmp":
            pc += op.arg
        elif op.oper == "nop":
            pc += 1
    return acc, pc


if __name__ == "__main__":
    debug = "--debug" in sys.argv
    program = parse_input(sys.argv[-1])
    for i, _ in enumerate(program):
        acc, pc = run_program(program)
        if pc == len(program):
            break
        if program[i].oper == "jmp":
            program[i].oper = "nop"
            acc, pc = run_program(program)
            if pc == len(program):
                log(f"jmp {program[i].arg} changed to nop (acc: {acc}, pc: {pc})")
                break
            program[i].oper = "jmp"
        if program[i].oper == "nop":
            program[i].oper = "jmp"
            acc, pc = run_program(program)
            if pc == len(program):
                log(f"nop {program[i].arg} changed to jmp (acc: {acc}, pc: {pc})")
                break
            program[i].oper = "nop"

    print(f"acc: {acc}, pc: {pc}")
