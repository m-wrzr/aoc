import copy
import math
import os

import numpy as np

__DIR__ = os.path.dirname(os.path.abspath(__file__))

filename, n_connections = "input.txt", 1_000


boxes: list[tuple[int, int, int]] = []


with open(os.path.join(__DIR__, filename), "r") as f:
    for line in f.readlines():
        boxes.append(tuple([int(x) for x in line.strip().split(",")]))  # type: ignore


def euclidean_distance(p: tuple[int, int, int], q: tuple[int, int, int]) -> float:
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 + (p[2] - q[2]) ** 2)


distance_matrix: list[list[float]] = []

for i, b_1 in enumerate(boxes):
    distance_matrix.append([])
    for j, b_2 in enumerate(boxes):
        if i == j:
            distance_matrix[i].append(float("inf"))
        else:
            distance_matrix[i].append(euclidean_distance(b_1, b_2))


def remove_smallest(matrix: list[list[float]]) -> tuple[list[list[float]], float, int, int]:
    min_val = float("inf")
    min_pos = (0, 0)

    for i, row in enumerate(matrix):
        for j, val in enumerate(row):
            if val < min_val:
                min_val = val
                min_pos = (i, j)

    i, j = min_pos
    # TODO: only half of matrix required...
    matrix[i][j] = float("inf")
    matrix[j][i] = float("inf")

    return matrix, min_val, i, j


def get_connected(x: tuple[int, int, int], connected: list[set]) -> set:
    for c in connected:
        if x in c:
            return c

    raise ValueError


def solve_1():
    connected: list[set] = [set([x]) for x in boxes]

    matrix = copy.deepcopy(distance_matrix)

    for _ in range(n_connections):
        matrix, _, i, j = remove_smallest(matrix)

        p = boxes[i]
        p_conn = get_connected(p, connected)

        q = boxes[j]
        q_conn = get_connected(q, connected)

        # print(f"{p=} {p_conn=}")
        # print(f"{q=} {q_conn=}")
        # print("-------")

        if p_conn != q_conn:
            connected.remove(p_conn)
            connected.remove(q_conn)
            connected.append(p_conn | q_conn)

    ## I think len()/2 connections?
    # always connect the two closest two boxes in each step, regardless if they are already connected

    # only consider three largest circuits
    sizes = sorted([len(x) for x in connected], reverse=True)[:3]
    # too low.. 1400
    print(f"1) {np.prod(sizes)}")


solve_1()


# this runs for a minute or two
def solve_2():
    connected: list[set] = [set([x]) for x in boxes]
    matrix = copy.deepcopy(distance_matrix)
    step = 0

    while True:
        print(f"Step {step}: {len(connected)} groups remaining")
        step += 1

        matrix, _, i, j = remove_smallest(matrix)

        p = boxes[i]
        p_conn = get_connected(p, connected)

        q = boxes[j]
        q_conn = get_connected(q, connected)

        # print(f"{p=} {p_conn=}")
        # print(f"{q=} {q_conn=}")
        # print("-------")

        if p_conn != q_conn:
            connected.remove(p_conn)
            connected.remove(q_conn)
            connected.append(p_conn | q_conn)

            if len(connected) == 1:
                print(f"2) {q[0] * p[0]}")
                break


solve_2()
