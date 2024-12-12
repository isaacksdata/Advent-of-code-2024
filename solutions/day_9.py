import logging
import sys

import fire
import numpy as np
import utilities
from main import main
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)


def format_gaps(data: list[int]) -> np.ndarray:
    new_data = []
    blocks = [x for i, x in enumerate(data) if i % 2 == 0]
    gaps = [x for i, x in enumerate(data) if i % 2 != 0]
    for i, block in enumerate(blocks):
        new_data.extend([i] * block)
        if i < len(gaps):
            new_data.extend([-1] * gaps[i])
    return np.array(new_data)


def find_first_gap(data: np.ndarray) -> int:
    return int(np.where(data == -1)[0][0])


def find_last_number(data: np.ndarray) -> int:
    return int(np.where(data != -1)[0][-1])


def checksum(data: np.ndarray) -> int:
    data[data == -1] = 0
    return int(np.sum(data * np.arange(data.shape[0])))


def solve_a(data: list[str]) -> int:
    data_input = [int(i) for i in list(data[0])]
    formatted_data = format_gaps(data_input)
    first_gap = find_first_gap(formatted_data)
    last_block = find_last_number(formatted_data)

    while first_gap < last_block:
        formatted_data[first_gap], formatted_data[last_block] = formatted_data[last_block], formatted_data[first_gap]
        first_gap = find_first_gap(formatted_data)
        last_block = find_last_number(formatted_data)
    return checksum(formatted_data)


def find_contigous_gaps(data: np.ndarray) -> list[tuple[int, int]]:
    indices = np.flatnonzero(data == -1)
    contiguous_regions = np.split(indices, np.where(np.diff(indices) != 1)[0] + 1)
    contiguous_regions_list = [(int(region[0]), int(region[-1] + 1)) for region in contiguous_regions]
    return contiguous_regions_list


def get_file(data: np.ndarray) -> list[tuple[int, int]]:
    blocks = [i for i in np.unique(data) if i >= 0]
    block_indices = []
    for block in blocks:
        indices = np.where(data == block)[0]
        block_indices.append((min(indices), max(indices)))
    block_indices.sort()
    block_indices.reverse()
    return block_indices


def move_file(
    gaps: list[tuple[int, int]], file: tuple[int, int], formatted_data: np.ndarray
) -> tuple[bool, np.ndarray]:
    l = (file[1] - file[0]) + 1
    for gap in gaps:
        if l <= max(gap) - min(gap) and gap[0] < file[0]:
            start = gap[0]
            end = gap[0] + l
            formatted_data[start:end], formatted_data[min(file) : max(file) + 1] = (
                formatted_data[min(file) : max(file) + 1],
                [-1] * l,
            )
            return True, formatted_data
    return False, formatted_data


def solve_b(data: list[str]) -> int:
    data_input = [int(i) for i in list(data[0])]
    formatted_data = format_gaps(data_input)
    files = get_file(formatted_data)
    gaps = find_contigous_gaps(formatted_data)
    for file in tqdm(files):
        moved, formatted_data = move_file(gaps, file, formatted_data)
        if moved:
            gaps = find_contigous_gaps(formatted_data)
    return checksum(formatted_data)


if __name__ == "__main__":
    sys.argv.append(f"--day={utilities.get_day(__file__)}")
    fire.Fire(main)
