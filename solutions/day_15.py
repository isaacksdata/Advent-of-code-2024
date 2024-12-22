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

DIRECTIONS = {
    "^": (-1, 0),
    "v": (1, 0),
    "<": (0, -1),
    ">": (0, 1),
}

ROBOT = "@"
BOX = "O"
WALL = "#"
EMPTY = "."
BIG_BOX_L = "["
BIG_BOX_R = "]"
BIG_BOXES = [BIG_BOX_L, BIG_BOX_R]


def gps_score(x: int, y: int) -> int:
    return (100 * x) + y


def solve_a(data: list[str], example: bool = False) -> int:
    arr, instructions = np.array([list(l) for l in data[: data.index("")]]), "".join(data[data.index("") + 1 :])
    x, y = np.where(arr == ROBOT)[0][0], np.where(arr == ROBOT)[1][0]
    arrays = []
    for in_id, move in enumerate(instructions):
        d = DIRECTIONS[move]
        new_x, new_y = x + d[0], y + d[1]
        if arr[new_x, new_y] == EMPTY:
            # easy move into an empty position
            arr[x, y] = EMPTY
            arr[new_x, new_y] = ROBOT
            x, y = new_x, new_y
            arrays.append(arr.copy())
        elif arr[new_x, new_y] == WALL:
            # nowhere to move to
            arrays.append(arr.copy())
            continue
        elif arr[new_x, new_y] == BOX:
            # here we need logic to figure out how the boxes will move
            if move == ">":
                boxes = np.where(arr[x, y:] == BOX)[0].tolist()
                boxes_to_move = []
                box = boxes[0]
                new_pos = box + d[1]
                if arr[x, new_pos + y] == WALL:
                    pass
                else:
                    boxes_to_move.append((box, new_pos))
                    while arr[x, new_pos + y] == BOX:
                        # add a new box
                        box = new_pos
                        new_pos = new_pos + d[1]
                        boxes_to_move.append((box, new_pos))
                    if arr[x, boxes_to_move[-1][1] + y] == EMPTY:
                        for box, new_box in reversed(boxes_to_move):
                            arr[x, box + y], arr[x, new_box + y] = arr[x, new_box + y], arr[x, box + y]
                        new_pos = y + d[1]
                        arr[x, y], arr[x, new_pos] = arr[x, new_pos], arr[x, y]
                        y = new_pos
                arrays.append(arr.copy())

            if move == "v":
                boxes = np.where(arr[x:, y] == BOX)[0].tolist()
                boxes_to_move = []
                box = boxes[0]
                new_pos = box + d[0]
                if arr[new_pos + x, y] == WALL:
                    pass
                else:
                    boxes_to_move.append((box, new_pos))
                    while arr[new_pos + x, y] in [BOX]:
                        box = new_pos
                        new_pos += d[0]
                        boxes_to_move.append((box, new_pos))
                    if arr[boxes_to_move[-1][1] + x, y] == EMPTY:
                        for box, new_box in reversed(boxes_to_move):
                            arr[box + x, y], arr[new_box + x, y] = arr[new_box + x, y], arr[box + x, y]
                        new_pos = x + d[0]
                        arr[x, y], arr[new_pos, y] = arr[new_pos, y], arr[x, y]
                        x = new_pos
                arrays.append(arr.copy())
            if move == "<":
                boxes = np.where(arr[x, :y] == BOX)[0].tolist()
                boxes.reverse()
                boxes_to_move = []
                box = boxes[0]
                new_pos = box + d[1]
                if arr[x, new_pos] == WALL:
                    pass
                else:
                    boxes_to_move.append((box, new_pos))
                    while arr[x, new_pos] == BOX:
                        box = new_pos
                        new_pos = new_pos + d[1]
                        boxes_to_move.append((box, new_pos))
                    if arr[x, boxes_to_move[-1][1]] == EMPTY:
                        for box, new_box in reversed(boxes_to_move):
                            arr[x, box], arr[x, new_box] = arr[x, new_box], arr[x, box]
                        new_pos = y + d[1]
                        arr[x, y], arr[x, new_pos] = arr[x, new_pos], arr[x, y]
                        y = new_pos
                arrays.append(arr.copy())
            if move == "^":
                boxes = np.where(arr[:x, y] == BOX)[0].tolist()
                boxes.reverse()
                boxes_to_move = []
                box = boxes[0]
                new_pos = box + d[0]
                if arr[new_pos, y] == WALL:
                    pass
                else:
                    boxes_to_move.append((box, new_pos))
                    while arr[new_pos, y] == BOX:
                        box = new_pos
                        new_pos = new_pos + d[0]
                        boxes_to_move.append((box, new_pos))
                    if arr[boxes_to_move[-1][1], y] == EMPTY:
                        for box, new_box in reversed(boxes_to_move):
                            arr[box, y], arr[new_box, y] = arr[new_box, y], arr[box, y]
                        new_pos = x + d[0]
                        arr[x, y], arr[new_pos, y] = arr[new_pos, y], arr[x, y]
                        x = new_pos
                arrays.append(arr.copy())

    # calculate final score
    boxes_coords = [(r, c) for r, c in zip(*np.where(arr == BOX))]
    total = sum([gps_score(i, j) for i, j in boxes_coords])

    return total


def solve_b(data: list[str], example: bool = False) -> int:
    # enlarge the map
    arr, instructions = np.array([list(l) for l in data[: data.index("")]]), "".join(data[data.index("") + 1 :])
    big_arr = np.zeros((arr.shape[0], arr.shape[1] * 2)).astype(arr.dtype)
    for i, j in zip(*np.where(arr == WALL)):
        big_arr[i, j * 2 : j * 2 + 2] = WALL
    for i, j in zip(*np.where(arr == EMPTY)):
        big_arr[i, j * 2 : j * 2 + 2] = EMPTY
    for i, j in zip(*np.where(arr == BOX)):
        big_arr[i, j * 2] = BIG_BOX_L
        big_arr[i, j * 2 + 1] = BIG_BOX_R
    small_x, small_y = np.where(arr == ROBOT)[0][0], np.where(arr == ROBOT)[1][0]
    big_arr[small_x, small_y * 2] = ROBOT
    big_arr[small_x, small_y * 2 + 1] = EMPTY
    x, y = np.where(arr == ROBOT)[0][0], np.where(big_arr == ROBOT)[1][0]
    # need a way of detecting bigger boxes - once we detect one side of the box we automatically know the other side
    for in_id, move in enumerate(instructions):
        lefts = [(r, c) for r, c in zip(*np.where(big_arr == BIG_BOX_L))]
        if not all([big_arr[l[0], l[1] + 1] == BIG_BOX_R for l in lefts]):
            raise ValueError("Boxes have been split!")
        d = DIRECTIONS[move]
        new_x, new_y = x + d[0], y + d[1]
        if big_arr[new_x, new_y] == EMPTY:
            # easy move into an empty position
            big_arr[x, y] = EMPTY
            big_arr[new_x, new_y] = ROBOT
            x, y = new_x, new_y
        elif big_arr[new_x, new_y] == WALL:
            # nowhere to move to
            continue
        elif big_arr[new_x, new_y] in BIG_BOXES:
            # here we need logic to figure out how the boxes will move
            if move == ">":
                boxes = np.where(big_arr[x, y:] == BIG_BOX_L)[0].tolist()
                if not boxes:
                    continue
                # we know that the tile to the right will always be BIG_BOX_R
                box_r = []
                for box in boxes:
                    box_r.append(box + 1)
                boxes.extend(box_r)
                boxes.sort()
                boxes_to_move = []
                box = boxes[0]
                new_pos = box + d[1]
                if big_arr[x, new_pos + y] == WALL:
                    pass
                else:
                    boxes_to_move.append((box, new_pos))
                    while big_arr[x, new_pos + y] in BIG_BOXES:
                        box = new_pos
                        new_pos = new_pos + d[1]
                        boxes_to_move.append((box, new_pos))
                    if big_arr[x, boxes_to_move[-1][1] + y] == EMPTY:
                        for box, new_box in reversed(boxes_to_move):
                            big_arr[x, box + y], big_arr[x, new_box + y] = big_arr[x, new_box + y], big_arr[x, box + y]
                        new_pos = y + d[1]
                        big_arr[x, y], big_arr[x, new_pos] = big_arr[x, new_pos], big_arr[x, y]
                        y = new_pos
            if move == "v":
                # grid is surrounded by walls so this will never raise indexerror
                nearest_wall = sorted(
                    [(i, y) for i in np.where(big_arr[x:, y] == WALL)[0].tolist()], key=lambda w: w[0]
                )[0]

                nearest_empty_list = sorted(
                    [(i, y) for i in np.where(big_arr[x:, y] == EMPTY)[0].tolist()], key=lambda w: w[0]
                )
                if nearest_empty_list:
                    nearest_empty = nearest_empty_list[0]
                    nearest_block = sorted([nearest_wall, nearest_empty], key=lambda w: w[0])[0]
                else:
                    nearest_block = nearest_wall
                boxes_l = [
                    (i, y) for i in np.where(big_arr[x:, y] == BIG_BOX_L)[0].tolist() if i + x < nearest_block[0] + x
                ]
                boxes_r = [
                    (i, y) for i in np.where(big_arr[x:, y] == BIG_BOX_R)[0].tolist() if i + x < nearest_block[0] + x
                ]
                box_lr = []
                for box in boxes_l:
                    box_lr.append((box[0], box[1] + 1))
                box_rl = []
                for box in boxes_r:
                    box_rl.append((box[0], box[1] - 1))
                boxes = sorted([*boxes_l, *boxes_r, *box_lr, *box_rl])
                if not boxes:
                    continue
                box = boxes[0]
                new_pos = (box[0] + d[0] + x, box[1])
                if big_arr[*new_pos] == WALL:
                    pass
                else:
                    # search for any other overlapping boxes
                    # sort by column (asc) and row (desc)
                    sorted_boxes = sorted(boxes, key=lambda b: (b[1], b[0]))
                    # create a queue and look for overlaps until the queue is empty
                    q = sorted_boxes.copy()
                    while q:
                        box = q.pop()
                        new_pos = (box[0] + d[0], box[1])
                        while big_arr[new_pos[0] + x, new_pos[1]] in BIG_BOXES:
                            if new_pos not in boxes:
                                # this is a new detected overlapping box
                                boxes.append(new_pos)
                                q.append((new_pos[0], new_pos[1]))
                                # we need to add both sides of the box
                                x_d = -1 if big_arr[new_pos[0] + x, new_pos[1]] == BIG_BOX_R else 1
                                boxes.append((new_pos[0], new_pos[1] + x_d))
                                q.append((new_pos[0], new_pos[1] + x_d))
                            new_pos = (new_pos[0] + d[0], new_pos[1])
                    boxes_to_move = [(b, (b[0] + 1, b[1])) for b in boxes]
                    # if any of the new positions in boxes_to_move are walls then can continue
                    if any(big_arr[b[1][0] + x, b[1][1]] == WALL for b in boxes_to_move):
                        continue
                    # now we have a list of boxes which could move up by one tile
                    # but we still need to check that all the top level boxes can actually move
                    col_tuples = {}
                    for box in boxes_to_move:
                        if box[1][1] not in col_tuples:
                            col_tuples[box[1][1]] = box[1]
                        else:
                            if box[1][0] > col_tuples[box[1][1]][0]:
                                col_tuples[box[1][1]] = box[1]
                    boxes_to_move = sorted(boxes_to_move, key=lambda b: (-b[0][0], b[0][1]))
                    if all(big_arr[b[0] + x, b[1]] == EMPTY for b in col_tuples.values()):
                        for box, new_box in boxes_to_move:
                            big_arr[box[0] + x, box[1]], big_arr[new_box[0] + x, new_box[1]] = (
                                big_arr[new_box[0] + x, new_box[1]],
                                big_arr[box[0] + x, box[1]],
                            )
                        new_pos = x + d[0]
                        big_arr[x, y], big_arr[new_pos, y] = big_arr[new_pos, y], big_arr[x, y]
                        x = new_pos
            if move == "<":
                boxes = np.where(big_arr[x, :y] == BIG_BOX_L)[0].tolist()
                if not boxes:
                    continue
                # we know that the tile to the right will always be BIG_BOX_R
                box_r = []
                for box in boxes:
                    box_r.append(box + 1)
                boxes.extend(box_r)
                boxes.sort()
                boxes.reverse()
                boxes_to_move = []
                box = boxes[0]
                new_pos = box + d[1]
                if big_arr[x, new_pos] == WALL:
                    pass
                else:
                    boxes_to_move.append((box, new_pos))
                    while big_arr[x, new_pos] in BIG_BOXES:
                        box = new_pos
                        new_pos = new_pos + d[1]
                        boxes_to_move.append((box, new_pos))
                    if big_arr[x, boxes_to_move[-1][1]] == EMPTY:
                        for box, new_box in reversed(boxes_to_move):
                            big_arr[x, box], big_arr[x, new_box] = big_arr[x, new_box], big_arr[x, box]
                        new_pos = y + d[1]
                        big_arr[x, y], big_arr[x, new_pos] = big_arr[x, new_pos], big_arr[x, y]
                        y = new_pos
            if move == "^":
                nearest_wall = sorted(
                    [(i, y) for i in np.where(big_arr[:x, y] == WALL)[0].tolist()], key=lambda w: -w[0]
                )[0]
                nearest_empty_list = sorted(
                    [(i, y) for i in np.where(big_arr[:x, y] == EMPTY)[0].tolist()], key=lambda w: -w[0]
                )
                if nearest_empty_list:
                    nearest_empty = nearest_empty_list[0]
                    nearest_block = sorted([nearest_wall, nearest_empty], key=lambda w: -w[0])[0]
                else:
                    nearest_block = nearest_wall
                boxes_l = [(i, y) for i in np.where(big_arr[:x, y] == BIG_BOX_L)[0].tolist() if i > nearest_block[0]]
                boxes_r = [(i, y) for i in np.where(big_arr[:x, y] == BIG_BOX_R)[0].tolist() if i > nearest_block[0]]
                box_lr = []
                for box in boxes_l:
                    box_lr.append((box[0], box[1] + 1))
                box_rl = []
                for box in boxes_r:
                    box_rl.append((box[0], box[1] - 1))
                boxes = sorted([*boxes_l, *boxes_r, *box_lr, *box_rl])
                if not boxes:
                    continue
                boxes.reverse()
                box = boxes[0]
                new_pos = (box[0] + d[0], box[1])
                if big_arr[*new_pos] == WALL:
                    pass
                else:
                    # search for any other overlapping boxes
                    # sort by column (asc) and row (desc)
                    sorted_boxes = sorted(boxes, key=lambda b: (b[1], -b[0]))
                    q = sorted_boxes.copy()
                    while q:
                        box = q.pop()
                        new_pos = (box[0] + d[0], box[1])
                        while big_arr[*new_pos] in BIG_BOXES:
                            if new_pos not in boxes:
                                # this is a new detected overlapping box
                                boxes.append(new_pos)
                                q.append(new_pos)
                                # we need to add both sides of the box
                                x_d = -1 if big_arr[*new_pos] == BIG_BOX_R else 1
                                boxes.append((new_pos[0], new_pos[1] + x_d))
                                q.append((new_pos[0], new_pos[1] + x_d))
                            new_pos = (new_pos[0] + d[0], new_pos[1])
                    boxes_to_move = [(b, (b[0] - 1, b[1])) for b in boxes]
                    # if any of the new positions in boxes_to_move are walls then can continue
                    if any(big_arr[*b[1]] == WALL for b in boxes_to_move):
                        continue
                    # now we have a list of boxes which could move up by one tile
                    # but we still need to check that all the top level boxes can actually move
                    col_tuples = {}
                    for box in boxes_to_move:
                        if box[1][1] not in col_tuples:
                            col_tuples[box[1][1]] = box[1]
                        else:
                            if box[1][0] < col_tuples[box[1][1]][0]:
                                col_tuples[box[1][1]] = box[1]
                    boxes_to_move = sorted(boxes_to_move, key=lambda b: (b[0][0], b[0][1]))
                    if all(big_arr[*b] == EMPTY for b in col_tuples.values()):
                        for box, new_box in boxes_to_move:
                            big_arr[*box], big_arr[*new_box] = big_arr[*new_box], big_arr[*box]
                        new_pos = x + d[0]
                        big_arr[x, y], big_arr[new_pos, y] = big_arr[new_pos, y], big_arr[x, y]
                        x = new_pos

    # calculate final score
    boxes_coords = [(r, c) for r, c in zip(*np.where(big_arr == BIG_BOX_L))]
    total = sum([gps_score(i, j) for i, j in boxes_coords])
    return total


if __name__ == "__main__":
    sys.argv.append(f"--day={utilities.get_day(__file__)}")
    fire.Fire(main)
