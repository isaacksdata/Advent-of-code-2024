import logging
import sys
from collections import deque
from typing import Optional

import fire
import numpy as np
import utilities
from main import main
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)

START = "S"
END = "E"
WALL = "#"
EMPTY = "."

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def bfs(
    arr: np.ndarray,
    start: tuple[int, int],
    end: tuple[int, int],
    cheat: tuple[int, int],
    invalid: str | int = WALL,
    max_steps: Optional[int] = None,
) -> tuple[int, list[tuple[int, int]], np.ndarray]:
    q = deque([start])
    path = [start]
    visited = np.zeros(arr.shape)
    ended = False
    while q:
        r, c = q.popleft()
        steps = visited[r, c]
        if max_steps is not None and steps > max_steps:
            break
        for rd, cd in DIRECTIONS:
            new_r, new_c = r + rd, c + cd
            if (
                0 <= new_r < arr.shape[0]
                and 0 <= new_c < arr.shape[1]
                and ((arr[new_r, new_c] != invalid) or ((new_r, new_c) in cheat))
                and visited[new_r, new_c] == 0
            ):
                visited[new_r, new_c] = steps + 1
                q.append((new_r, new_c))
                if (new_r, new_c) == end:
                    ended = True
                    break
        if ended:
            break

    visited[*start] = 0
    if not ended:
        for i in range(1, int(np.max(visited))):
            path.extend([(i, j) for i, j in zip(*np.where(visited == i))])
        return -1, path, visited
    for i in range(1, int(visited[*end] + 1)):
        path.append((int(np.where(visited == i)[0][0]), int(np.where(visited == i)[1][0])))
    return visited[*end], path, visited


def solve_a(data: list[str], example: bool = False) -> int:
    saving = 2 if example else 100
    arr = np.array([list(l) for l in data])
    start = (int(np.where(arr == START)[0][0]), int(np.where(arr == START)[1][0]))
    end = (int(np.where(arr == END)[0][0]), int(np.where(arr == END)[1][0]))
    steps, path, _ = bfs(arr, start, end, (-1, -1))

    walls = set([(x, y) for x, y in zip(*np.where(arr == WALL))])
    walls = {(w_x, w_y) for w_x, w_y in walls if (0 < w_x < arr.shape[0] - 1 and 0 < w_y < arr.shape[1] - 1)}
    walls = {(w_x, w_y) for w_x, w_y in walls if (sum(arr[w_x + dx, w_y + dy] == WALL for dx, dy in DIRECTIONS) < 3)}
    walls = {(w_x, w_y) for w_x, w_y in walls if (sum((w_x + dx, w_y + dy) in path for dx, dy in DIRECTIONS) > 0)}

    count = 0
    for w_x, w_y in tqdm(walls):
        cheat_steps, _, _ = bfs(arr, start, end, (w_x, w_y))
        if steps - cheat_steps >= saving:
            count += 1
    return count


def manhattan_distance(x: tuple[int, ...], y: tuple[int, ...]) -> int:
    return sum(abs(c1 - c2) for c1, c2 in zip(x, y))


def solve_b(data: list[str], example: bool = False) -> int:
    # i think that for part B we should move away from BFS
    # if we have the list of coords on path then we can iterate over each position in the path and see if a shortcut
    # exists to a later point in the path which would use no more than 20 seconds
    saving = 50 if example else 100
    arr = np.array([list(l) for l in data])
    start = (int(np.where(arr == START)[0][0]), int(np.where(arr == START)[1][0]))
    end = (int(np.where(arr == END)[0][0]), int(np.where(arr == END)[1][0]))
    steps, path, visited = bfs(arr, start, end, (-1, -1))
    visited[*start] = 0
    cheat_limit = 20

    # first working solution used a nested for loop which took about 3mins
    # vectorised numpy solutions takes ~1s
    path_np = np.array(path)
    count = 0
    for i, p in tqdm(enumerate(path), total=len(path)):
        if i + 3 >= len(path):  # + 3 avoids testing neighbours in the path
            break
        candidates = path_np[i + 3 :]

        distances = np.abs(candidates - p).sum(axis=1)

        valid_indices = (distances <= cheat_limit) & ((np.arange(len(candidates)) + i + 3 - i) > distances)
        reductions = (np.arange(len(candidates)) + i + 3 - i)[valid_indices] - distances[valid_indices]

        count += np.sum(reductions >= saving)
    return count


if __name__ == "__main__":
    sys.argv.append(f"--day={utilities.get_day(__file__)}")
    sys.argv.append("--part=b")
    sys.argv.append("--expected_sample=285")
    fire.Fire(main)
