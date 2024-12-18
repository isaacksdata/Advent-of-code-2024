import logging
import math
import re
import sys
from collections import namedtuple
from itertools import chain

import fire
import utilities
from main import main

logging.basicConfig(level=logging.INFO)


MUL_PATTERN = r"mul\(\d{1,3},\d{1,3}\)"
DIGITS_PATTERN = r"\d{1,3},\d{1,3}"

instruction = namedtuple("instruction", ["operation", "index"])


def process_mul_operator(muls: list[str]) -> int:
    return sum(
        [math.prod(list(map(int, digits.split(",")))) for mul in muls for digits in re.findall(DIGITS_PATTERN, mul)]
    )


def solve_a(data: list[str], example: bool = False) -> int:
    total = 0
    for i in data:
        valid_muls = re.findall(MUL_PATTERN, i)

        total += process_mul_operator(valid_muls)
    return total


def solve_b(data: list[str], example: bool = False) -> int:
    string = "".join(data)

    donts = [instruction(operation=0, index=k.start()) for k in re.finditer(r"don't\(\)", string)]
    dos = [instruction(operation=1, index=k.start()) for k in re.finditer(r"do\(\)", string)]

    number_line: list[instruction] = sorted([*dos, *donts], key=lambda x: x.index)

    valid_text = []

    current_do = 1
    idx = 0

    for val in number_line:
        if current_do == val.operation:
            continue
        if current_do == 1 and val.operation == 0:
            valid_text.append(string[idx : val.index])
        idx = val.index
        current_do = val.operation

        if current_do == 1:
            valid_text.append(string[idx:])

    muls = list(chain(*[re.findall(MUL_PATTERN, j) for j in valid_text]))

    total = process_mul_operator(muls)
    return total


if __name__ == "__main__":
    sys.argv.append(f"--day={utilities.get_day(__file__)}")
    fire.Fire(main)
