import os
from collections import Counter

__DIR__ = os.path.dirname(os.path.abspath(__file__))

filename = "input.large.txt"


# calculate
# - area
# - perimeter

garden: list[list[str]] = []

ct_areas: Counter[str] = Counter()
ct_fences: Counter[str] = Counter()

with open(os.path.join(__DIR__, filename), "r") as f:
    garden = [list(li.strip()) for li in f.readlines()]


N, M = len(garden), len(garden[0])

directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def get_free_index(g: list[list[str]]) -> tuple[int, int] | tuple[None, None]:
    for i in range(N):
        for j in range(M):
            if g[i][j]:
                return i, j

    return None, None


def is_valid_index(i, j) -> bool:
    return i >= 0 and j >= 0 and i < N and j < M


def is_oob_major(i, j):
    return i < -1 or j < -1 or i > N + 1 or j > M + 1


def get_region(
    g: list[list[str]],
    i,
    j,
    visited: set[tuple[int, int]],
) -> set[tuple[int, int]]:
    if (i, j) in visited:
        raise ValueError("should not visit this")
    else:
        visited.add((i, j))

    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    for d in directions:
        i_new, j_new = i - d[0], j - d[1]
        if (
            is_valid_index(i_new, j_new)
            and g[i_new][j_new] == g[i][j]
            and (i_new, j_new) not in visited
        ):
            r = get_region(g, i_new, j_new, visited)
            visited.update(r)

    return visited


def calc_area(nodes: set[tuple[int, int]]) -> int:
    return len(nodes)


def calc_perimeter_1(nodes: set[tuple[int, int]]) -> int:
    ct = 0

    for i, j in nodes:
        for d in directions:
            i_next, j_next = i - d[0], j - d[1]

            if not is_valid_index(i_next, j_next):
                ct += 1
            elif (i_next, j_next) not in nodes:
                ct += 1

    return ct


def calc_perimeter_2(nodes: set[tuple[int, int]]):
    def is_top(i, k):
        return (i, j) in nodes and (i - 1, j) not in nodes

    def is_bottom(i, j):
        return (i, j) in nodes and (i + 1, j) not in nodes

    def is_left(i, j):
        return (i, j) in nodes and (i, j - 1) not in nodes

    def is_right(i, j):
        return (i, j) in nodes and (i, j + 1) not in nodes

    ct, i_s, j_s = 0, [i for i, _ in nodes], [j for _, j in nodes]

    # check all from  TOP to BOTTOM
    for i in range(min(i_s), max(i_s) + 1):
        top_active, bottom_active = False, False

        for j in range(min(j_s), max(j_s) + 1):
            if is_top(i, j):
                # we flipped, was no edge before here
                if not top_active:
                    ct += 1
                top_active = True
            else:
                top_active = False

            if is_bottom(i, j):
                if not bottom_active:
                    ct += 1
                bottom_active = True
            else:
                bottom_active = False

    for j in range(min(j_s), max(j_s) + 1):
        left_active, right_active = False, False

        for i in range(min(i_s), max(i_s) + 1):
            if is_left(i, j):
                if not left_active:
                    ct += 1
                left_active = True
            else:
                left_active = False

            if is_right(i, j):
                if not right_active:
                    ct += 1
                right_active = True
            else:
                right_active = False

    return ct


i, j = get_free_index(garden)

regions: list[tuple[str, set[tuple[int, int]]]] = []


agg = 0

while i is not None and j is not None:
    region = get_region(garden, i, j, set())

    a, p = calc_area(region), calc_perimeter_2(region)
    print(garden[i][j], a, p)
    agg += a * p

    for ia, ja in region:
        garden[ia][ja] = ""

    i, j = get_free_index(garden)


print(agg)
