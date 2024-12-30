import importlib
import logging
import os
from typing import Optional

import utilities
from constants import YEAR


def main(
    day: int = 1, part: str = "a", expected_sample: Optional[int] = None, test: bool = False, force_test: bool = False
) -> None:
    path_prefix = "../" if os.getcwd().endswith("solutions") else "./"
    sample = utilities.read_sample_data(f"{path_prefix}data/day_{day}_{part}.txt")

    module_name = f"day_{day}"

    module = importlib.import_module(module_name)
    solve_a = getattr(module, "solve_a")
    solve_b = getattr(module, "solve_b")

    func = solve_a if part == "a" else solve_b
    if expected_sample is not None:
        sample_answer = func(sample, example=True)
        assert sample_answer == expected_sample, f"Failed Sample! Expected {expected_sample} but got {sample_answer}"
        logging.info("Sample Succeeded!")
    else:
        logging.info("Skipping sample!")

    if force_test:
        logging.info("Force Testing! This runs the example data but does not verify the answer!")
        sample_answer = func(sample, example=True)
        logging.info("Test answer = %s", sample_answer)

    if not test:
        puzzle = utilities.format_input_data(utilities.get_puzzle(year=YEAR, day=day))

        answer = func(puzzle)
        logging.info("Puzzle Answer = %s!", answer)

        utilities.submit_answer(answer=answer, year=YEAR, day=day, part=part)
