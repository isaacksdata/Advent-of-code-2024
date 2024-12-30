import logging
import sys
from itertools import product

import fire
import numpy as np
import utilities
from main import main

logging.basicConfig(level=logging.INFO)


def get_lock_heights(arr: np.ndarray) -> list[int]:
    return np.argmax(arr[::-1] == "#", axis=0) * -1 + arr.shape[0] - 1


def get_key_heights(arr: np.ndarray) -> list[int]:
    h = np.argmax(arr == "#", axis=0)
    shift = [6 if x > 0 else 0 for x in h]
    return (shift - h).tolist()


def get_heights(arr: np.ndarray, is_lock: bool = True) -> list[int]:
    return get_lock_heights(arr) if is_lock else get_key_heights(arr)


def solve_a(data: list[str], example: bool = False) -> int:
    current_pattern = []
    keys = []
    locks = []
    for i, row in enumerate(data):
        if row != "" and i < len(data) - 1:
            current_pattern.append(row)
        else:
            if i == len(data) - 1:
                current_pattern.append(row)
            if all(j == "#" for j in current_pattern[0]) and all(j == "." for j in current_pattern[-1]):
                locks.append(np.array([list(l) for l in current_pattern]))
            else:
                keys.append(np.array([list(l) for l in current_pattern]))
            current_pattern = []
    lock_heights = [get_heights(arr, is_lock=True) for arr in locks]
    key_heights = [get_heights(arr, is_lock=False) for arr in keys]

    combos = 0
    fits = []
    max_h = locks[0].shape[0] - 1
    for i, (l, k) in enumerate(product(lock_heights, key_heights)):
        if np.all(l + k < max_h):
            combos += 1
            fits.append([l, k])

    return combos


def solve_b(data: list[str], example: bool = False) -> int:
    return 0


if __name__ == "__main__":
    sys.argv.append(f"--day={utilities.get_day(__file__)}")
    sys.argv.append(f"--part=a")
    sys.argv.append(f"--expected_sample=3")
    fire.Fire(main)
