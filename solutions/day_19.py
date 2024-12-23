import logging
import sys
from functools import lru_cache

import fire
import utilities
from main import main
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)


@lru_cache
def make_match_all(string: str, patterns: tuple[str, ...]) -> int:
    if string == "":
        return 1
    matches = [t for t in patterns if string.startswith(t)]
    if matches:
        return sum([make_match_all(string[len(m) :], patterns) for m in matches])
    else:
        return 0


def solve_a(data: list[str], example: bool = False) -> int:
    towels = data[0].split(", ")
    displays = data[2:]
    count = 0
    for display in displays:
        count += make_match_all(display, tuple(towels)) > 0
    return count


def solve_b(data: list[str], example: bool = False) -> int:
    towels = data[0].split(", ")
    displays = data[2:]
    count = 0
    for display in tqdm(displays):
        count += make_match_all(display, tuple(towels))
    return count


if __name__ == "__main__":
    sys.argv.append(f"--day={utilities.get_day(__file__)}")
    fire.Fire(main)
