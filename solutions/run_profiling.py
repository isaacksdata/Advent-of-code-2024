import importlib
import logging
import os
import time

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import utilities
import yaml
from constants import YEAR

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    days = range(1, 26)
    parts = ["a", "b"]

    path_prefix = "../" if os.getcwd().endswith("solutions") else "./"

    with open(f"{path_prefix}answers/examples.yaml", "r") as file:
        example_answers = yaml.safe_load(file)
    with open(f"{path_prefix}answers/puzzles.yaml", "r") as file:
        puzzle_answers = yaml.safe_load(file)

    times = pd.DataFrame(columns=["day", "part", "mode", "answer", "time"])

    for day in days:
        puzzle = utilities.format_input_data(utilities.get_puzzle(year=YEAR, day=day))

        module_name = f"day_{day}"
        module = importlib.import_module(module_name)
        solve_a = getattr(module, "solve_a")
        solve_b = getattr(module, "solve_b")

        for part in parts:
            if day == 25 and part == "b":
                continue
            sample = utilities.read_sample_data(f"{path_prefix}data/day_{day}_{part}.txt")
            func = solve_a if part == "a" else solve_b

            logging.info("####### Day %s Part %s #######", day, part)

            logging.info("## Example ##")

            run_test = False if ((day == 14 and part == "b") or (day == 25 and part == "b")) else True

            if run_test:
                start = time.time()
                response = func(sample, example=True)
                assert (
                    response == example_answers[f"day{day}"][part]
                ), f"Failed example for day {day}, part {part}, response {response}"
                end = time.time()
                length = end - start
            else:
                length = 0
                response = 0
            times.loc[len(times)] = [day, part, "example", response, length]

            logging.info("## Puzzle ##")

            start = time.time()
            response = func(puzzle)
            assert (
                response == puzzle_answers[f"day{day}"][part]
            ), f"Failed puzzle for day {day}, part {part}, response {response}"
            end = time.time()
            length = end - start
            times.loc[len(times)] = [day, part, "puzzle", response, length]

    times.to_csv(f"{path_prefix}profiling.csv", index=False)

    for mode in ["example", "puzzle"]:
        sns.lineplot(times.query(f"mode =='{mode}'"), x="day", y="time", hue="part", marker="o")
        plt.ylabel("Time (s)")
        plt.savefig(f"{mode}_profiling.png")
        plt.close()
