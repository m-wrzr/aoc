import itertools
import os

from shapely import Polygon, box

__DIR__ = os.path.dirname(os.path.abspath(__file__))

filename = "input.txt"


tiles: list[tuple[int, int]] = []


with open(os.path.join(__DIR__, filename), "r") as f:
    for line in f.readlines():
        tiles.append(tuple([int(x) for x in line.strip().split(",")]))  # type: ignore


def solve_1():

    max_size = 0

    for (x_1, y_1), (x_2, y_2) in itertools.combinations(tiles, 2):
        x_diff = abs(x_1 - x_2) + 1
        y_diff = abs(y_1 - y_2) + 1

        max_size = max(x_diff * y_diff, max_size)

    print(f"1) {max_size}")


solve_1()


def solve_2():

    polygon = Polygon(tiles)
    max_size = 0

    for (x_1, y_1), (x_2, y_2) in itertools.combinations(tiles, 2):
        x_diff = abs(x_1 - x_2) + 1
        y_diff = abs(y_1 - y_2) + 1

        rect = box(min(x_1, x_2), min(y_1, y_2), max(x_1, x_2), max(y_1, y_2))

        if polygon.covers(rect):
            max_size = max(x_diff * y_diff, max_size)

    print(f"2) {max_size}")


solve_2()
