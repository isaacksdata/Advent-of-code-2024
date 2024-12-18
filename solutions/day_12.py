import logging
import sys
from typing import Any

import fire
import numpy as np
import skimage
import utilities
from main import main
from skimage.measure._regionprops import RegionProperties

logging.basicConfig(level=logging.INFO)

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def get_plant_regions(arr: np.ndarray, plant: int) -> tuple[np.ndarray, list[RegionProperties]]:
    plant_arr = arr.copy()
    plant_arr[arr == plant] = 1
    plant_arr[arr != plant] = 0
    plant_arr = plant_arr.astype(int)

    # set connectivity to 1 to avoid connecting by diagonals
    labels = skimage.measure.label(plant_arr, connectivity=1)
    objects = skimage.measure.regionprops(labels)
    return labels, objects


def get_perimeter(
    labels: np.ndarray, object: RegionProperties, rows: int, cols: int
) -> tuple[int, set[tuple[int, int, int, int]]]:
    perimeter_coords = set()
    perimeter = 0
    for row, col in [(r, c) for r, c in zip(*np.where(labels == object.label))]:
        for dr, dc in DIRECTIONS:
            neighbor_row, neighbor_col = int(row + dr), int(col + dc)
            if (
                neighbor_row < 0
                or neighbor_row >= rows
                or neighbor_col < 0
                or neighbor_col >= cols
                or labels[neighbor_row, neighbor_col] != object.label
            ):
                perimeter += 1
                perimeter_coords.add((neighbor_row, neighbor_col, dr, dc))
    return perimeter, perimeter_coords


def solve_a(data: list[str], example: bool = False) -> int:
    arr = np.array([list(l) for l in data])
    plants = np.unique(arr)
    total = 0
    rows, cols = arr.shape
    for plant in plants:
        labels, objects = get_plant_regions(arr, plant)

        for object in objects:
            perimeter, perimeter_coords = get_perimeter(labels, object, rows, cols)
            total += object.area * perimeter
    return total


def solve_b(data: list[str], example: bool = False) -> int:
    arr = np.array([list(l) for l in data])
    plants = np.unique(arr)
    total = 0
    rows, cols = arr.shape
    for plant in plants:
        labels, objects = get_plant_regions(arr, plant)
        for object in objects:
            perimeter, perimeter_coords = get_perimeter(labels, object, rows, cols)

            # for part B we need to analyse the perimeter coords to find adjacent coordinates which together
            # equate to a side
            n_sides = 0

            # we use a while loop to keep going until we have classified all coordinates on the perimeter to a side
            while perimeter_coords:
                # r = row number
                # c = col number
                # dr = direction of view for row
                # dc = direction of view for col
                r, c, dr, dc = perimeter_coords.pop()  # get a coordinate from the perimeter

                # first check to find potential neighbours from the perimeter
                potential_neighbours = [
                    (pr, pc, pdr, pdc)
                    for pr, pc, pdr, pdc in perimeter_coords
                    if ((pdr, pdc) == (dr, dc) and (pr == r or pc == c))
                ]

                potential_neighbours.append((r, c, dr, dc))
                potential_neighbours.sort()
                true_neighbours = []
                start = potential_neighbours[0]
                # now we try to exhaustively find all potential perimeter neighbours based on our coordinates so far
                # this prevents portions of sides being found and multi counting of sides in later iterations
                while True:
                    new_ns = [
                        (pr, pc, pdr, pdc)
                        for pr, pc, pdr, pdc in perimeter_coords
                        if (
                            (pdr, pdc) == (start[2], start[3])
                            and (pr == start[0] or pc == start[1])
                            and (pr, pc, pdr, pdc) not in potential_neighbours
                        )
                    ]
                    if not new_ns:
                        break
                    potential_neighbours.extend(new_ns)
                    potential_neighbours.sort()
                    start = potential_neighbours[0]

                # now we have a list of potential neighbours for the popped coordinates, we choose a coordinate after
                # sorting and add neighbours until we have a complete side
                true_neighbours.append(start)
                while True:
                    connections = [
                        n
                        for n in potential_neighbours
                        if (
                            (n[0], n[1]) in [(start[0] + i, start[1] + j) for i, j in DIRECTIONS]
                            and n not in true_neighbours
                        )
                    ]
                    if not connections:
                        # no more neighbours can be added
                        break
                    true_neighbours.append(connections[0])
                    start = connections[0]

                if (r, c, dr, dc) not in true_neighbours:
                    # this means there are multiple sides in the same row or column which are not all connected
                    # so we need to re add the original popped coordinate as we did assign it to a side
                    perimeter_coords.add((r, c, dr, dc))

                # remove the assigned coords from our list so we do not see them again
                for n in true_neighbours:
                    if n in perimeter_coords:
                        perimeter_coords.remove(n)
                n_sides += 1
            total += object.area * n_sides
    return total


if __name__ == "__main__":
    sys.argv.append(f"--day={utilities.get_day(__file__)}")
    fire.Fire(main)
