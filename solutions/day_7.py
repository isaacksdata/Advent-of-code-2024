import itertools
import logging
import operator
import sys
from functools import lru_cache
from typing import Callable

import fire
import numpy as np
import utilities
from main import main
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)


ops = [operator.add, operator.mul]


def concatenate(a: int, b: int) -> int:
    return int(str(a) + str(b))


@lru_cache
def calc(ops: tuple[Callable], numbers: tuple[int]) -> int:
    total = numbers[0]
    for i, op in enumerate(ops):
        total = op(total, numbers[i + 1])
    return total


def solve_equation(equation: str, operations: list[Callable]) -> int:
    answer, numbers = equation.split(": ")
    numbers_int = [int(i) for i in numbers.split()]
    n_ops = len(numbers_int) - 1
    possibles = list(itertools.product(operations, repeat=n_ops))
    for p in possibles:
        res = calc(tuple(p), tuple(numbers_int))
        if res == int(answer):
            return res
    return 0


def solve_a(data: list[str], example: bool = False) -> int:
    total = 0
    for equation in tqdm(data):
        res = solve_equation(equation, ops)
        total += res
    return total


# todo this takes too long (~2mins) so there must be a short cut
def solve_b(data: list[str], example: bool = False) -> int:
    total = 0
    ops.append(concatenate)
    for equation in tqdm(data):
        res = solve_equation(equation, ops)
        total += res
    return total


if __name__ == "__main__":
    sys.argv.append(f"--day={utilities.get_day(__file__)}")
    fire.Fire(main)
