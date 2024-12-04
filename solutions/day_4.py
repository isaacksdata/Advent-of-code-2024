import logging
import sys
from collections import defaultdict
from typing import Optional

import fire
import numpy as np
import utilities
from main import main

logging.basicConfig(level=logging.INFO)

DIRECTIONS: list[tuple[int, int]] = [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)]

DIAGONALS: dict[str, tuple[int, int]] = {"tl": (-1, -1), "tr": (-1, 1), "br": (1, 1), "bl": (1, -1)}

mapping: dict[str, int] = {"X": 1, "M": 2, "A": 3, "S": 4}


def move(r: int, c: int, direction: tuple[int, int]) -> tuple[int, int]:
    return r + direction[0], c + direction[1]


def has_valid_neighbour(
    arr: np.ndarray,
    row: int,
    col: int,
    value: int,
    idx: list[tuple[int, int]],
    dir: Optional[tuple[int, int]] = None,
) -> tuple[bool, list[list[tuple[int, int]]]]:
    if dir is None:
        neighbours: list[tuple[tuple[int, int], tuple[int, int]]] = [
            ((row + i, col + j), (i, j)) for i, j in DIRECTIONS
        ]
    else:
        # only assess neighbours in the existing direction
        neighbours = [((row + dir[0], col + dir[1]), dir)]
    matches: list[list[tuple[int, int]]] = []
    for n, d in neighbours:
        sub_idx = idx.copy()
        if not all(x >= 0 for x in n):
            continue
        try:
            valid = arr[n[0], n[1]] == value
        except IndexError:
            # trying to access outside of array
            continue
        if valid:
            sub_idx.append(n)
            if value == mapping.get("S"):
                # XMAS complete
                matches.append(sub_idx)
            else:
                # the letter in current direction could be part of XMAS so go a step further
                _, sub_matches = has_valid_neighbour(arr, n[0], n[1], value + 1, dir=d, idx=sub_idx.copy())
                if sub_matches:
                    matches.append(sub_matches[0])
    return len(matches) > 0, matches


def to_formatted_array(data: list[str]) -> np.ndarray:
    arr = np.asarray([list(d) for d in data])
    arr = np.where(np.isin(arr, list(mapping.keys())), arr, 0)
    for letter, num in mapping.items():
        arr[arr == letter] = num
    arr = arr.astype(np.int8)
    return arr


def solve_a(data: list[str]) -> int:
    arr = to_formatted_array(data)

    # find potential start points - the Xs
    row_coords, col_coords = np.where(arr == mapping.get("X"))
    total = 0
    matches = []
    for r, c in zip(row_coords, col_coords):
        result, idx = has_valid_neighbour(arr, r, c, mapping.get("M", 0), idx=[(r, c)])
        if result:
            total += len(idx)
            matches.extend(idx)
    return total


def check_diagonals(
    arr: np.ndarray,
    r: int,
    c: int,
    m1: tuple[int, int],
    m2: tuple[int, int],
) -> tuple[bool, Optional[list[tuple[int, int]]]]:
    # check top coordinate
    t_coord = move(r, c, m1)
    if any(x < 0 for x in t_coord):
        # bail out if the coordinate is not possible
        return False, None
    t_val = arr[t_coord]

    # if the top val is M or S then continue to checking the opposite corner
    if t_val in [mapping.get("M"), mapping.get("S")]:
        try:
            b_coord = move(r, c, m2)
            if any(x < 0 for x in b_coord):
                # bail out if the coordinate is not possible
                return False, None
            b_val = arr[b_coord]
        except IndexError:
            return False, None
        if (t_val == mapping.get("M") and b_val == mapping.get("S")) or (
            t_val == mapping.get("S") and b_val == mapping.get("M")
        ):
            return True, [(r, c), *[move(r, c, d) for d in DIAGONALS.values()]]
    return False, None


def solve_b(data: list[str]) -> int:
    # this time we will start with As and find the MAS crosses
    arr = to_formatted_array(data)
    row_coords, col_coords = np.where(arr == mapping.get("A"))
    total = 0
    matches: list[tuple[int, int]] = []
    for r, c in zip(row_coords, col_coords):
        # first check top left and bottom right
        if check_diagonals(arr=arr, r=r, c=c, m1=DIAGONALS.get("tl", (0, 0)), m2=DIAGONALS.get("br", (0, 0)))[0]:
            # no we check the other diagonal
            res, idx = check_diagonals(
                arr=arr, r=r, c=c, m1=DIAGONALS.get("tr", (0, 0)), m2=DIAGONALS.get("bl", (0, 0))
            )
            if res and idx is not None:
                total += 1
                matches.extend(idx)
    return total


if __name__ == "__main__":
    sys.argv.append(f"--day={utilities.get_day(__file__)}")
    fire.Fire(main)
