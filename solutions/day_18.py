import logging
import sys
from collections import deque

import fire
import numpy as np
import utilities
from main import main

logging.basicConfig(level=logging.INFO)

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
CORRUPT = 1


def bfs(arr: np.ndarray, start: tuple[int, int], end: tuple[int, int]) -> int:
    q = deque([start])

    visited = np.zeros_like(arr)
    ended = False
    while q:
        r, c = q.popleft()
        steps = visited[r, c]
        for rd, cd in DIRECTIONS:
            new_r, new_c = r + rd, c + cd
            if (
                0 <= new_r < arr.shape[0]
                and 0 <= new_c < arr.shape[1]
                and arr[new_r, new_c] != CORRUPT
                and visited[new_r, new_c] == 0
            ):
                visited[new_r, new_c] = steps + 1
                q.append((new_r, new_c))
                if (new_r, new_c) == end:
                    ended = True
                    break
        if ended:
            break
    if not ended:
        return -1
    return visited[*end]


def initialise(data: list[str], example: bool = False) -> tuple[np.ndarray, int]:
    if example:
        shape = (7, 7)
        n = 12
    else:
        shape = (71, 71)
        n = 1024
    arr = np.zeros(shape)
    for i in data[:n]:
        y, x = i.split(",")
        arr[int(x), int(y)] = 1
    return arr, n


def solve_a(data: list[str], example: bool = False) -> int:
    arr, _ = initialise(data, example)
    steps = bfs(arr, (0, 0), (arr.shape[0] - 1, arr.shape[1] - 1))
    return steps


def solve_b(data: list[str], example: bool = False) -> str:
    arr, n = initialise(data, example)
    i = ""
    for i in data[n:]:
        y, x = i.split(",")
        arr[int(x), int(y)] = 1
        steps = bfs(arr, (0, 0), (arr.shape[0] - 1, arr.shape[1] - 1))
        if steps == -1:
            break
    return i


if __name__ == "__main__":
    sys.argv.append(f"--day={utilities.get_day(__file__)}")
    sys.argv.append("--part=b")
    sys.argv.append("--expected_sample='6,1'")
    fire.Fire(main)
