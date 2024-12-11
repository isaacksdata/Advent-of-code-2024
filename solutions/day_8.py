import itertools
import logging
import sys

import fire
import numpy as np
import utilities
from main import main
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)


def find_antinodes_direction_one(pair: tuple[tuple[int, int], tuple[int, int]], r_d: int, c_d: int) -> tuple[int, int]:
    if r_d == 0:
        node = (pair[0][0], pair[0][1] - abs(c_d))
    elif c_d == 0:
        node = (pair[0][0] - abs(r_d), pair[0][1])
    elif c_d > 0:
        node = (pair[0][0] - abs(r_d), pair[0][1] + abs(c_d))
    elif c_d < 0:
        node = (pair[0][0] - abs(r_d), pair[0][1] - abs(c_d))
    else:
        raise ValueError("Unexpected values for r_d and c_d")
    return node


def find_antinodes_direction_two(pair: tuple[tuple[int, int], tuple[int, int]], r_d: int, c_d: int) -> tuple[int, int]:
    if r_d == 0:
        node = (pair[0][0], pair[1][1] + abs(c_d))
    elif c_d == 0:
        node = (pair[1][0] + abs(r_d), pair[1][1])
    elif c_d > 0:
        node = (pair[1][0] + abs(r_d), pair[1][1] - abs(c_d))
    elif c_d < 0:
        node = (pair[1][0] + abs(r_d), pair[1][1] + abs(c_d))
    else:
        raise ValueError("Unexpected values for r_d and c_d")
    return node


def is_valid_antinode(node: tuple[int, int], arr: np.ndarray) -> bool:
    return not any(x < 0 for x in node) and node[0] < arr.shape[0] and node[1] < arr.shape[1]


def solve_a(data: list[str]) -> int:
    arr = np.array([list(a) for a in data])
    signals = [i for i in np.unique(arr) if i != "."]
    antinodes: list[tuple[int, int]] = []
    for signal in signals:
        antennas = [(r, c) for r, c in zip(*np.where(arr == signal))]
        for pair in itertools.combinations(antennas, 2):
            r_d = pair[0][0] - pair[1][0]
            c_d = pair[0][1] - pair[1][1]

            node_1 = find_antinodes_direction_one(pair, r_d, c_d)
            node_2 = find_antinodes_direction_two(pair, r_d, c_d)

            # if so then find the expected positions of the antinodes and see if both are in the area of the array
            antinodes.extend([node for node in [node_1, node_2] if is_valid_antinode(node, arr)])
    return len(set(antinodes))


def solve_b(data: list[str]) -> int:
    arr = np.array([list(a) for a in data])
    signals = [i for i in np.unique(arr) if i != "."]
    antinodes: list[tuple[int, int]] = []
    for signal in tqdm(signals):
        antennas = [(r, c) for r, c in zip(*np.where(arr == signal))]
        antinodes.extend(antennas)
        for pair in itertools.combinations(antennas, 2):
            r_d = pair[0][0] - pair[1][0]
            c_d = pair[0][1] - pair[1][1]

            # find antinodes in one direction
            node_1 = find_antinodes_direction_one(pair, r_d, c_d)
            node_2 = find_antinodes_direction_two(pair, r_d, c_d)
            iter_r_d = r_d
            iter_c_d = c_d
            while is_valid_antinode(node_1, arr):
                antinodes.append(node_1)
                iter_r_d = iter_r_d + r_d
                iter_c_d = iter_c_d + c_d
                node_1 = find_antinodes_direction_one(pair, iter_r_d, iter_c_d)

            iter_r_d = r_d
            iter_c_d = c_d
            while is_valid_antinode(node_2, arr):
                antinodes.append(node_2)
                iter_r_d = iter_r_d + r_d
                iter_c_d = iter_c_d + c_d
                node_2 = find_antinodes_direction_two(pair, iter_r_d, iter_c_d)
    return len(set(antinodes))


if __name__ == "__main__":
    sys.argv.append(f"--day={utilities.get_day(__file__)}")
    fire.Fire(main)
