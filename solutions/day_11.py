import logging
import sys
from collections import Counter
from functools import lru_cache

import fire
import utilities
from main import main

logging.basicConfig(level=logging.INFO)


def replace_stone(stone: int) -> tuple[bool, int]:
    if stone != 0:
        return False, stone
    return True, 1


def split_stone(stone: int) -> tuple[bool, list[int] | int]:
    digits = str(stone)
    s = len(digits)
    if stone < 10 or s % 2 != 0:
        return False, stone
    l, r = digits[: s // 2], digits[s // 2 :]
    return True, [int(l), int(r)]


def multiply_stone(stone: int) -> tuple[bool, int]:
    return True, stone * 2024


funcs = [replace_stone, split_stone, multiply_stone]


@lru_cache
def change_stone(stone: int) -> int | list[int]:
    new_stone: list[int] | int = 0
    for func in funcs:
        changed, new_stone = func(stone)
        if changed:
            break
    return new_stone


def change_stones(stone_counts: dict[int, int]) -> dict[int, int]:
    new_counts: dict[int, int] = {}
    for stone, counts in stone_counts.items():
        new_stone = change_stone(stone)
        if isinstance(new_stone, int):
            if new_stone in new_counts:
                new_counts[new_stone] += counts
            else:
                new_counts[new_stone] = counts
        else:
            for s in new_stone:
                if s in new_counts:
                    new_counts[s] += counts
                else:
                    new_counts[s] = counts
    return new_counts


def solve_a(data: list[str]) -> int:
    stones = [int(i) for i in data[0].split()]
    stone_counts = dict(Counter(stones))
    blinks = 25
    for _ in range(blinks):
        stone_counts = change_stones(stone_counts)
    return sum(list(stone_counts.values()))


def solve_b(data: list[str]) -> int:
    stones = [int(i) for i in data[0].split()]
    stone_counts = dict(Counter(stones))
    blinks = 75
    for _ in range(blinks):
        stone_counts = change_stones(stone_counts)
    return sum(list(stone_counts.values()))


if __name__ == "__main__":
    sys.argv.append(f"--day={utilities.get_day(__file__)}")
    fire.Fire(main)
