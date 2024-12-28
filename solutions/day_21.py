import logging
import sys
from collections import Counter
from typing import Any

import fire
import numpy as np
import utilities
from main import main
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
GAP = -1
A_BUTTON = 10
NUMERIC_KEYPAD = np.array([[7, 8, 9], [4, 5, 6], [1, 2, 3], [GAP, 0, A_BUTTON]])
UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
MOVE_TO_TUPLE: dict[int, tuple[int, int]] = {0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1), 10: (0, 0)}
DIRECTIONAL_KEYPAD = np.array([[GAP, UP, A_BUTTON], [LEFT, DOWN, RIGHT]])
NUM_TO_MOVE = {0: "^", 1: "v", 2: "<", 3: ">", 10: "A", "A": "A"}

VALID_NUMERIC = {
    (i, j): NUMERIC_KEYPAD[i, j]
    for i in range(NUMERIC_KEYPAD.shape[0])
    for j in range(NUMERIC_KEYPAD.shape[1])
    if NUMERIC_KEYPAD[i, j] != -1
}

VALID_DIRECTIONAL = {
    (i, j): DIRECTIONAL_KEYPAD[i, j]
    for i in range(DIRECTIONAL_KEYPAD.shape[0])
    for j in range(DIRECTIONAL_KEYPAD.shape[1])
    if DIRECTIONAL_KEYPAD[i, j] != -1
}


def get_coordinates(arr: np.ndarray, element: int) -> tuple[int, int]:
    return [(x, y) for x, y in zip(*np.where(arr == element))][0]


NUMERIC_GAP = get_coordinates(NUMERIC_KEYPAD, GAP)
DIRECTION_GAP = get_coordinates(DIRECTIONAL_KEYPAD, GAP)


def get_start(arr: np.ndarray) -> tuple[int, int]:
    return get_coordinates(arr, A_BUTTON)


def get_moves(y: int, x: int) -> tuple[list[int] | list[Any], list[int] | list[Any]]:
    x_moves, y_moves = [], []
    if x != 0:
        m = UP if x < 0 else DOWN
        x_moves = [m] * abs(x)
    if y != 0:
        m = LEFT if y < 0 else RIGHT
        y_moves = [m] * abs(y)
    return x_moves, y_moves


def solve_code(code: list[str | int] | str, keypad: np.ndarray, valid_moves: dict[tuple[int, int], int]) -> list[str]:
    moves = []
    position = get_start(keypad)
    for digit in tqdm(code):
        digit = A_BUTTON if digit == "A" else digit
        x, y = get_coordinates(keypad, int(digit))
        x_d, y_d = x - position[0], y - position[1]
        x_moves, y_moves = get_moves(y_d, x_d)  # swap round to y, x so it moves vertically first and avoids the GAPs
        # check to see if the position is below the gap
        # if so add y moves first, then x, otherwise x then y
        if (x, position[1]) in valid_moves and y_d > 0:
            moves_string = "".join([*map(str, x_moves), *map(str, y_moves), NUM_TO_MOVE[A_BUTTON]])
        elif (position[0], y) in valid_moves:
            moves_string = "".join([*map(str, y_moves), *map(str, x_moves), NUM_TO_MOVE[A_BUTTON]])
        else:
            moves_string = "".join([*map(str, x_moves), *map(str, y_moves), NUM_TO_MOVE[A_BUTTON]])
        position = (x, y)
        moves.append(moves_string)
    return moves


def solve_a(data: list[str], example: bool = False) -> int:
    total = 0
    for code in data:
        moves_1 = "".join(solve_code(list(code), NUMERIC_KEYPAD, VALID_NUMERIC))
        moves_2 = "".join(solve_code(list(moves_1), DIRECTIONAL_KEYPAD, VALID_DIRECTIONAL))
        moves_3 = "".join(solve_code(list(moves_2), DIRECTIONAL_KEYPAD, VALID_DIRECTIONAL))
        complexity = len(moves_3) * int(code[:-1])
        total += complexity
    return total


def solve_b(data: list[str], example: bool = False) -> int:
    total = 0
    n = 25
    for code in data:
        moves = ["".join(solve_code(list(code), NUMERIC_KEYPAD, VALID_NUMERIC))]
        routines = Counter(moves)
        all_routes = [routines]
        for _ in tqdm(range(n)):
            new_routes = []
            for route in all_routes:
                new_routines: Counter = Counter()
                for k, v in route.items():
                    # here we will find new movement patterns and increment the counts for already seen patterns
                    new_counts = Counter(solve_code(k, DIRECTIONAL_KEYPAD, VALID_DIRECTIONAL))
                    for k, v2 in new_counts.items():
                        new_counts[k] *= v
                    new_routines.update(new_counts)
                new_routes.append(new_routines)
            all_routes = new_routes

        # we might have a key pattern like 012A which is equivalent to 4 button presses hence the len(k)
        complexity = sum([len(k) * v for k, v in all_routes[0].items()]) * int(code[:-1])
        total += complexity
    return total


if __name__ == "__main__":
    sys.argv.append(f"--day={utilities.get_day(__file__)}")
    sys.argv.append("--part=a")
    sys.argv.append("--expected_sample=126384")
    fire.Fire(main)
