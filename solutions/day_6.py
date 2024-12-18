import logging
import sys

import fire
import numpy as np
import utilities
from main import main
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)

START = "^"
BLOCK = "#"

DIRECTIONS = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}


def move_in_direction(
    arr: np.ndarray, current_position: tuple[int, int], direction: str
) -> tuple[tuple[int, int], bool]:
    """
    Move as far as possible in given direction
    """
    r, c = current_position
    next_position = current_position
    exit = False
    if direction == "down":
        if BLOCK in arr[r:, c]:
            next_position = (int(np.min(np.where(arr[r:, c] == "#"))) + r - 1, c)
        else:
            next_position = (arr.shape[0] - 1, c)
            exit = True
    if direction == "up":
        if BLOCK in arr[:r, c]:
            next_position = (int(np.max(np.where(arr[:r, c] == "#"))) + 1, c)
        else:
            next_position = (0, c)
            exit = True
    if direction == "left":
        if BLOCK in arr[r, :c]:
            next_position = (r, int(np.max(np.where(arr[r, :c] == "#"))) + 1)
        else:
            next_position = (r, 0)
            exit = True
    if direction == "right":
        if BLOCK in arr[r, c:]:
            next_position = (r, int(np.min(np.where(arr[r, c:] == "#"))) + c - 1)
        else:
            next_position = (r, arr.shape[1] - 1)
            exit = True

    return next_position, exit


def change_direction(current_direction: str) -> str:
    if current_direction == "up":
        return "right"
    if current_direction == "down":
        return "left"
    if current_direction == "left":
        return "up"
    return "down"


def walk(
    arr: np.ndarray, current_position: tuple[int, int], current_direction: str, check_loop: bool = False
) -> tuple[list[tuple[int, int]], bool]:
    exited = False
    turn_points = [current_position]
    turn_points_and_directions = []
    while not exited:
        if check_loop:
            if (current_position, current_direction) in turn_points_and_directions:
                return turn_points, True
            turn_points_and_directions.append((current_position, current_direction))
        current_position, exited = move_in_direction(arr, current_position, current_direction)
        current_direction = change_direction(current_direction)
        turn_points.append(current_position)
    return turn_points, False


def fill_route(arr: np.ndarray, turn_points: list[tuple[int, int]]) -> np.ndarray:
    z = np.zeros(arr.shape)
    for i, p in enumerate(turn_points[:-1]):
        p2 = turn_points[i + 1]

        if p[0] == p2[0]:  # Same row
            row = p[0]
            col_start, col_end = sorted([p[1], p2[1]])
            z[row, col_start : col_end + 1] = 1
        elif p[1] == p2[1]:  # Same column
            col = p[1]
            row_start, row_end = sorted([p[0], p2[0]])
            z[row_start : row_end + 1, col] = 1
    return z


def solve_a(data: list[str], example: bool = False) -> int:
    arr = np.array([list(l) for l in data])
    r, c = np.where(arr == START)
    current_position = (int(r[0]), int(c[0]))
    current_direction = "up"
    turn_points, _ = walk(arr, current_position, current_direction)
    z = fill_route(arr, turn_points)
    return int(np.sum(z))


def solve_b(data: list[str], example: bool = False) -> int:
    arr = np.array([list(l) for l in data])
    r, c = np.where(arr == START)
    current_position = (int(r[0]), int(c[0]))
    current_direction = "up"
    initial_turn_points, _ = walk(arr, current_position, current_direction)
    z = fill_route(arr, initial_turn_points)
    route_coords = np.where(z == 1)

    # iterate over route coords and test for infinite loop
    n_loops = 0
    for r_b, c_b in tqdm(zip(route_coords[0], route_coords[1])):
        new_arr = np.copy(arr)
        new_arr[r_b, c_b] = BLOCK
        _, looped = walk(new_arr, current_position, current_direction, check_loop=True)
        if looped:
            n_loops += 1
    return n_loops


if __name__ == "__main__":
    sys.argv.append(f"--day={utilities.get_day(__file__)}")

    fire.Fire(main)
