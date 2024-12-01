import logging
import sys
from collections import Counter

import fire
import utilities
from main import main

logging.basicConfig(level=logging.INFO)


def get_lists(data: list[str]) -> tuple[list[int], list[int]]:
    lefts = []
    rights = []
    for i in data:
        l, r = i.split()
        lefts.append(int(l))
        rights.append(int(r))
    return lefts, rights


def solve_a(data: list[str]) -> int:
    # sample = 11
    lefts, rights = get_lists(data)
    lefts = sorted(lefts)
    rights = sorted(rights)

    distance = sum([abs(l - r) for l, r in zip(lefts, rights)])
    return distance


def solve_b(data: list[str]) -> int:
    # sample = 31
    lefts, rights = get_lists(data)
    right_counts = Counter(rights)
    total = sum([l * right_counts.get(l, 0) for l in lefts])
    return total


if __name__ == "__main__":
    sys.argv.append(f"--day={utilities.get_day(__file__)}")
    fire.Fire(main)
