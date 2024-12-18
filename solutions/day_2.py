import logging
import sys

import fire
import utilities
from main import main

logging.basicConfig(level=logging.INFO)


MAX_CHANGE = 3


def check_report(report: list[int]) -> bool:
    # 0 = unset, -1 = decreasing, 1 = increasing
    direction = 0

    for i, x in enumerate(report):
        if i == 0:
            continue
        diff = x - report[i - 1]
        if diff == 0:
            return False
        elif abs(diff) > MAX_CHANGE:
            return False
        current_direction = 1 if diff > 0 else -1

        if direction == 0:
            direction = current_direction

        if direction != current_direction:
            return False
    return True


def check_report_with_dampener(report: list[int]) -> bool:
    full_report_result = check_report(report)
    if full_report_result:
        return full_report_result
    for i, x in enumerate(report):
        sub_list = [y for j, y in enumerate(report) if j != i]
        if check_report(sub_list):
            return True
    return False


def solve_a(data: list[str], example: bool = False) -> int:
    result = [check_report(list(map(int, report.split()))) for report in data]
    return sum(result)


def solve_b(data: list[str], example: bool = False) -> int:
    result = [check_report_with_dampener(list(map(int, report.split()))) for report in data]
    return sum(result)


if __name__ == "__main__":
    sys.argv.append(f"--day={utilities.get_day(__file__)}")
    fire.Fire(main)
