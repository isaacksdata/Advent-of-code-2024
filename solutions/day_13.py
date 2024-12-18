import logging
import re
import sys
from typing import Optional

import fire
import numpy as np
import utilities
from main import main
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)

COST_A = 3
COST_B = 1
PRIZE_OFFSET = 10000000000000
ROUNDING_FACTOR = 3


def solve_equations(a_x: int, a_y: int, b_x: int, b_y: int, prize_x: int, prize_y: int) -> tuple[float, float]:
    A = np.array([[a_x, b_x], [a_y, b_y]])
    B = np.array([prize_x, prize_y])

    a_pushes, b_pushes = np.linalg.solve(A, B)
    return a_pushes, b_pushes


def solve_machine(
    a: str, b: str, prize: str, offset: int, max_pushes: float | int
) -> tuple[Optional[int], Optional[int]]:
    a_x, a_y = list(map(int, re.findall(r"\d+", a)))
    b_x, b_y = list(map(int, re.findall(r"\d+", b)))
    prize_x, prize_y = list(map(int, re.findall(r"\d+", prize)))
    prize_x += offset
    prize_y += offset

    # we use linear algebra to solve the system of linear equations
    A = np.array([[a_x, b_x], [a_y, b_y]])
    B = np.array([prize_x, prize_y])

    a_pushes, b_pushes = np.linalg.solve(A, B)

    if (
        round(a_pushes, ROUNDING_FACTOR).is_integer()
        and round(b_pushes, ROUNDING_FACTOR).is_integer()
        and a_pushes <= max_pushes
        and b_pushes <= max_pushes
    ):
        return int(round(a_pushes, ROUNDING_FACTOR)), int(round(b_pushes, ROUNDING_FACTOR))
    return None, None


def solve_a(data: list[str]) -> int:
    data = [d for d in data if d != ""]
    machines = [data[i : i + 3] for i in range(0, len(data), 3)]
    total = 0
    for a, b, prize in tqdm(machines):
        a_pushes, b_pushes = solve_machine(a, b, prize, 0, 101)
        if a_pushes is not None and b_pushes is not None:
            total += (a_pushes * COST_A) + (b_pushes * COST_B)
    return total


def solve_b(data: list[str]) -> int:
    data = [d for d in data if d != ""]
    machines = [data[i : i + 3] for i in range(0, len(data), 3)]
    total = 0
    for a, b, prize in tqdm(machines):
        a_pushes, b_pushes = solve_machine(a, b, prize, PRIZE_OFFSET, np.inf)
        if a_pushes is not None and b_pushes is not None:
            total += (a_pushes * COST_A) + (b_pushes * COST_B)
    return total


if __name__ == "__main__":
    sys.argv.append(f"--day={utilities.get_day(__file__)}")
    fire.Fire(main)
