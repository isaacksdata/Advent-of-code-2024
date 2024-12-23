import heapq
import logging
import sys
from typing import Optional

import fire
import numpy as np
import utilities
from main import main

logging.basicConfig(level=logging.INFO)

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
START = "S"
END = "E"
WALL = "#"
EMPTY = "."

# some customised types
MAZE_TILE = tuple[int, int, int, tuple[int, int], list[tuple[int, int]]]
COORD = tuple[int, int]


def run_maze_with_dijkstra(
    arr: np.ndarray,
    start_pos: Optional[COORD] = None,
    direction: Optional[COORD] = None,
) -> tuple[int, list[COORD], dict[COORD, int]]:
    rows, cols = arr.shape
    if start_pos is None:
        start_pos = (int(np.where(arr == START)[0][0]), int(np.where(arr == START)[1][0]))
    direction = (0, 1) if direction is None else direction
    end_pos = (int(np.where(arr == END)[0][0]), int(np.where(arr == END)[1][0]))

    # Priority queue: (cumulative_cost, (row, col), direction of travel, path so far)
    # this means we take low cost paths first
    pq: list[MAZE_TILE] = [(0, start_pos[0], start_pos[1], direction, [])]
    visited: dict[COORD, int] = {}

    while pq:
        cost, r, c, direction, path = heapq.heappop(pq)

        # seen it before with a lower cost so safe to ignore
        if (r, c) in visited and visited[(r, c)] <= cost:
            continue
        visited[(r, c)] = cost

        # extend with new tile
        path = path + [(r, c)]

        # because djikstra prioritises low cost paths, we can assume that the first time we get to the END
        # it will be lowest cost route
        if (r, c) == end_pos:
            return cost, path, visited

        # neighbours are the adjacent nodes
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            new_direction = (dr, dc)

            if 0 <= nr < rows and 0 <= nc < cols and arr[nr, nc] != WALL:
                score_delta = 1001 if direction and new_direction != direction else 1
                heapq.heappush(pq, (cost + score_delta, nr, nc, new_direction, path))

    return -1, [], visited


def solve_a(data: list[str], example: bool = False) -> int:
    arr = np.array([list(l) for l in data])
    score, path, _ = run_maze_with_dijkstra(arr)
    return score


def solve_b(data: list[str], example: bool = False) -> int:
    arr = np.array([list(l) for l in data])
    score, path, visited = run_maze_with_dijkstra(arr)
    new_tiles = []
    stack = list(reversed(path))
    tracked = []
    while stack:
        r, c = stack.pop()
        if (r, c) in tracked:
            continue
        # check for neighbours which are not in path
        neighbours = [((r + dr, c + dc), (dr, dc)) for dr, dc in DIRECTIONS]
        neighbours = [n for n in neighbours if n[0] not in path and arr[*n[0]] == EMPTY]
        # for each neighbour, run djikstra from that neighbour
        for new_pos, direction in neighbours:
            if new_pos not in path:
                new_r, new_c = new_pos
                new_score, new_path, new_visited = run_maze_with_dijkstra(
                    arr,
                    start_pos=(new_r, new_c),
                    direction=direction,
                )
                # then add the score to the score in visited for that tile
                tile_score = visited.get((new_r, new_c), None)
                if tile_score is not None:
                    if tile_score + new_score == score:
                        # if the score is equal to the original score then add the parts of new path to total path
                        new_tiles.extend(new_path)
                        stack.extend(new_path)
        tracked.append((r, c))
    all_tiles = {*path, *new_tiles}
    return len(all_tiles)


if __name__ == "__main__":
    sys.argv.append(f"--day={utilities.get_day(__file__)}")
    fire.Fire(main)
