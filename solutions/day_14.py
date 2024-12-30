import logging
import re
import sys
from dataclasses import dataclass
from typing import Optional

import fire
import numpy as np
import utilities
from main import main

logging.basicConfig(level=logging.INFO)


BASE_LINE_LENGTH = 5


@dataclass
class Robot:
    x: int
    y: int
    x_speed: int
    y_speed: int


def sanitise_coords(x: int, y: int, rows: int, cols: int) -> tuple[int, int]:
    if x < 0:
        x = cols + x
    if x >= cols:
        x = x - cols
    if y < 0:
        y = rows + y
    if y >= rows:
        y = y - rows
    return x, y


def collect_robots(data: list[str]) -> dict[int, Robot]:
    robots = {}
    for i, robot in enumerate(data):
        pos, speed = robot.split(" ")
        # x is number of tiles from left
        # y is number of tiles from top
        x, y = list(map(int, re.findall(r"-?\d+", pos)))
        x_speed, y_speed = list(map(int, re.findall(r"-?\d+", speed)))
        robots[i + 1] = Robot(x, y, x_speed, y_speed)
    return robots


def _move_robots(robots: dict[int, Robot], rows: int, cols: int) -> dict[int, Robot]:
    for robot_id, robot in robots.items():
        new_x = robot.x + robot.x_speed
        new_y = robot.y + robot.y_speed
        new_x, new_y = sanitise_coords(new_x, new_y, rows, cols)
        robot.x = new_x
        robot.y = new_y
    return robots


def is_neighbor(p: tuple[int, int], q: tuple[int, int]) -> bool:
    x, y = p
    neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    return q in neighbors


def longest_continuous_line(pixels: list[tuple[int, int]]) -> list[tuple[int, int]]:
    longest_line: list[tuple[int, int]] = []
    for i, point in enumerate(pixels[:-1]):
        current_line = []
        p = point
        counter = 1

        while is_neighbor(p, pixels[i + counter]):
            current_line.append(p)
            p = pixels[i + counter]
            counter += 1
            if i + counter == len(pixels):
                break
        if len(current_line) > len(longest_line):
            longest_line = current_line
    return longest_line


def check_is_christmas(robots: dict[int, Robot]) -> bool:
    robot_coords = sorted([(robot.y, robot.x) for _, robot in robots.items()])
    # a christmas tree might have a base e.g. a line of robots
    line = longest_continuous_line(robot_coords)
    return len(line) > BASE_LINE_LENGTH


def move_robots(
    robots: dict[int, Robot],
    rows: int,
    cols: int,
    seconds: Optional[int] = None,
) -> tuple[dict[int, Robot], int]:
    if seconds is not None:
        for _ in range(seconds):
            robots = _move_robots(robots, rows, cols)
        counter = seconds
    else:
        its_christmas = False
        counter = 0
        while not its_christmas:
            robots = _move_robots(robots, rows, cols)
            counter += 1
            its_christmas = check_is_christmas(robots)
    return robots, counter


def solve_a(data: list[str], example: bool = False) -> int:
    rows = 7 if example else 103
    cols = 11 if example else 101
    seconds = 100
    arr = np.zeros((rows, cols))
    robots = collect_robots(data)

    robots, _ = move_robots(robots, rows, cols, seconds)

    finish_arr = np.zeros_like(arr)
    for i, robot in robots.items():
        finish_arr[robot.y, robot.x] += 1

    q1 = np.sum(finish_arr[0 : finish_arr.shape[0] // 2, 0 : finish_arr.shape[1] // 2])
    q2 = np.sum(finish_arr[0 : finish_arr.shape[0] // 2, finish_arr.shape[1] // 2 + 1 :])
    q3 = np.sum(finish_arr[finish_arr.shape[0] // 2 + 1 :, 0 : finish_arr.shape[1] // 2])
    q4 = np.sum(finish_arr[finish_arr.shape[0] // 2 + 1 :, finish_arr.shape[1] // 2 + 1 :])

    return q1 * q2 * q3 * q4


def solve_b(data: list[str], example: bool = False) -> int:
    rows = 7 if example else 103
    cols = 11 if example else 101

    robots = collect_robots(data)

    robots, seconds = move_robots(robots, rows, cols, seconds=None)

    return seconds


if __name__ == "__main__":
    sys.argv.append(f"--day={utilities.get_day(__file__)}")
    sys.argv.append("--part=b")
    sys.argv.append("--expected_sample=None")
    fire.Fire(main)
