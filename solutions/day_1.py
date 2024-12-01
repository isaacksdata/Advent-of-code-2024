import logging
from collections import Counter

import fire
import utilities
from constants import YEAR


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


def main(day: int = 1, part: str = "a", expected_sample: int = 0, test: bool = False) -> None:
    sample = utilities.read_sample_data(f"data/day_{day}_{part}.txt")

    func = solve_a if part == "a" else solve_b

    assert func(sample) == expected_sample, "Failed Sample!"
    logging.info("Sample Succeeded!")

    if not test:
        puzzle = utilities.format_input_data(utilities.get_puzzle(year=YEAR, day=day))

        answer = func(puzzle)

        utilities.submit_answer(answer=answer, year=YEAR, day=day, part=part)


if __name__ == "__main__":
    fire.Fire(main)
