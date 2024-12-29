import logging
import sys
import time
from collections import Counter
from typing import Any

import fire
import numpy as np
import utilities
from main import main
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)


def mix(a: int, b: int) -> int:
    return a ^ b


def prune(a: int, m: int = 16777216) -> int:
    return a % m


def step(a: int) -> int:
    # part 1
    a = prune(mix(a, a * 64))

    # part 2
    a = prune(mix(a, a // 32))

    # part 3
    a = prune(mix(a, a * 2048))

    return a


def solve_a(data: list[str], example: bool = False) -> int:
    formatted_data = list(map(int, data))
    n = 2000
    secrets = []
    for secret in formatted_data:
        for _ in range(n):
            secret = step(secret)
        secrets.append(secret)
    return sum(secrets)


def solve_b(data: list[str], example: bool = False) -> int:
    formatted_data = list(map(int, data))

    n = 2000

    prices_arr = np.zeros((len(formatted_data), n))

    for i, secret in tqdm(enumerate(formatted_data), total=len(formatted_data)):
        for j in range(n):
            secret = step(secret)
            prices_arr[i, j] = int(str(secret)[-1])

    # compute differences along a row
    diff_arr = np.zeros_like(prices_arr)
    diff_arr[:, 1:] = prices_arr[:, 1:] - prices_arr[:, :-1]

    # generate the 4mer sequences
    sequences = np.lib.stride_tricks.sliding_window_view(diff_arr, window_shape=4, axis=1)
    unique_sequences = np.unique(sequences.reshape(-1, 4), axis=0)

    # we generate hashes for each sequence as this lets us use "==" instead of np.all later which is much faster
    unique_hashes = np.dot(unique_sequences, [1, 256, 65536, 16777216])
    sequence_hashes = np.dot(sequences, [1, 256, 65536, 16777216])

    # concat 0 column so that we can return 0 if the sequence is not found in a row and get 0 bananas
    prices_arr = np.hstack((np.zeros((prices_arr.shape[0], 1)), prices_arr))

    bananas = 0
    for seq in tqdm(unique_hashes, total=len(unique_hashes)):
        matches = sequence_hashes == seq
        first_indices = np.where(np.any(matches, axis=1), np.argmax(matches, axis=1), 0)

        # add 4 to get the last index (4 because we concatenated a column of 0s in index 0)
        shift_arr = np.array([4 if i != 0 else 0 for i in first_indices])
        first_indices += shift_arr

        bananas = max(np.sum(prices_arr[np.arange(prices_arr.shape[0]), first_indices]), bananas)

    return bananas


if __name__ == "__main__":
    sys.argv.append(f"--day={utilities.get_day(__file__)}")
    sys.argv.append("--part=b")
    sys.argv.append("--expected_sample=23")
    fire.Fire(main)
