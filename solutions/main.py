import importlib
import logging

import utilities
from constants import YEAR


def main(day: int = 1, part: str = "a", expected_sample: int = 0, test: bool = False) -> None:
    sample = utilities.read_sample_data(f"data/day_{day}_{part}.txt")

    module_name = f"day_{day}"

    module = importlib.import_module(module_name)
    solve_a = getattr(module, "solve_a")
    solve_b = getattr(module, "solve_b")

    func = solve_a if part == "a" else solve_b
    sample_answer = func(sample)
    assert sample_answer == expected_sample, f"Failed Sample! Expected {expected_sample} but got {sample_answer}"
    logging.info("Sample Succeeded!")

    if not test:
        puzzle = utilities.format_input_data(utilities.get_puzzle(year=YEAR, day=day))

        answer = func(puzzle)

        utilities.submit_answer(answer=answer, year=YEAR, day=day, part=part)
