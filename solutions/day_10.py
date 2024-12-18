import logging
import sys
from typing import Callable
from typing import Optional

import fire
import numpy as np
import utilities
from main import main
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
MAX_HEIGHT = 9


def check_height(v: int, h: int) -> bool:
    return v == h


def follow_trail(arr: np.ndarray, trailhead: tuple[int, int], condition_fn: Callable, recursive: bool = False) -> int:
    """
    This is a DFS implementation for following a path in a 2D array.
    """
    rows, cols = arr.shape
    visited = np.zeros_like(arr, dtype=bool)
    stack = [trailhead]
    complete_paths = []

    def is_valid(r: int, c: int, h: int) -> bool:
        return 0 <= r < rows and 0 <= c < cols and (not visited[r, c] or recursive) and condition_fn(arr[r, c], h)

    def dfs_recursive(r: int, c: int, path: Optional[list[tuple[int, int]]] = None) -> None:
        """Recursive DFS implementation."""
        if path is None:
            path = []
        visited[r, c] = True
        path.append((r, c))

        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            current_height = int(arr[r, c])
            next_height = current_height + 1
            if current_height == MAX_HEIGHT and path not in complete_paths:
                # this is the point where the trail reaches a peak by some unique path
                # i.e. what we want to count for part B
                complete_paths.append(path)

            if is_valid(nr, nc, next_height):
                dfs_recursive(nr, nc, path.copy())

    if recursive:
        r, c = trailhead
        if is_valid(r, c, 0):
            dfs_recursive(r, c)
        return len(complete_paths)
    else:
        # for part A we just want to see how many MAX_HEIGHT entries can be reached from trailhead
        # but we do not care how we got there
        path = []
        while stack:
            r, c = stack.pop()
            current_height = int(arr[r, c])
            next_height = current_height + 1

            if not visited[r, c]:
                visited[r, c] = True
                path.append((r, c))

                for dr, dc in DIRECTIONS:
                    nr, nc = r + dr, c + dc
                    if is_valid(nr, nc, next_height):
                        stack.append((nr, nc))

        path_heights = [arr[p[0], p[1]] for p in list(set(path))]
        return len([h for h in path_heights if h == MAX_HEIGHT])


def solve_a(data: list[str], example: bool = False) -> int:
    arr = np.array([list(l) for l in data]).astype(int)
    total = 0
    trailheads = [(r, c) for r, c in zip(*np.where(arr == 0))]
    for trailhead in tqdm(trailheads):
        total += follow_trail(arr, trailhead, check_height, recursive=False)
    return total


def solve_b(data: list[str], example: bool = False) -> int:
    arr = np.array([list(l) for l in data]).astype(int)
    total = 0
    trailheads = [(r, c) for r, c in zip(*np.where(arr == 0))]
    for trailhead in tqdm(trailheads):
        total += follow_trail(arr, trailhead, check_height, recursive=True)
    return total


if __name__ == "__main__":
    sys.argv.append(f"--day={utilities.get_day(__file__)}")
    fire.Fire(main)
