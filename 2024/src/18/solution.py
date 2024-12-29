import os

import networkx as nx

__DIR__ = os.path.dirname(os.path.abspath(__file__))

filename = "input.large.txt"

# 70
GRID_RANGE = 70


dirs = {
    ">": (0, 1),
    "<": (0, -1),
    "^": (-1, 0),
    "v": (1, 0),
}

corrupted_all: list[tuple[int, int]] = []

with open(os.path.join(__DIR__, filename), "r") as f:
    for i, line in enumerate(f.readlines()):
        corrupted_all.append(tuple([int(x) for x in line.split(",")]))  # type: ignore

# this runs a while ...
# improve either with binary search for first result
# or search from the back with re-adding edges (only one graph construction)
for sub in range(1020, len(corrupted_all) + 1):
    corrupted = corrupted_all[:sub]
    G = nx.Graph()
    print(sub)

    for y in range(GRID_RANGE + 1):
        for x in range(GRID_RANGE + 1):
            if (x, y) in corrupted:
                continue

            G.add_node((x, y))

            for dir in dirs.values():
                x_next = x + dir[1]
                y_next = y + dir[0]

                if (
                    0 <= x_next <= GRID_RANGE
                    and 0 <= y_next <= GRID_RANGE
                    and (x_next, y_next) not in corrupted
                ):
                    G.add_edge((x, y), (x_next, y_next))

    try:
        path = nx.shortest_path(G, (0, 0), (GRID_RANGE, GRID_RANGE))

        if sub == 1024:
            print(f"Solution 1) {len(path) - 1}")

    except Exception:
        print(f"Solution 2) {corrupted_all[sub - 1]}")
        break
