import os

import networkx as nx

__DIR__ = os.path.dirname(os.path.abspath(__file__))

filename = "input.large.txt"


pos_start = pos_end = (0, 0)
maze: list[list[str]] = []

DG = nx.DiGraph()


def print_maze():
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            print(maze[i][j], end="")
        print()


dirs: dict[str, tuple[int, int]] = {
    ">": (0, 1),
    "<": (0, -1),
    "^": (-1, 0),
    "v": (1, 0),
}

with open(os.path.join(__DIR__, filename), "r") as f:
    for i, line in enumerate(f.readlines()):
        line = line.strip()

        maze.append([])
        for j, element in enumerate(list(line)):
            if element == "S":
                pos_start = (i, j)
            elif element == "E":
                pos_end = (i, j)

            maze[i].append(element)

            if element == "#":
                continue

            for k in dirs.keys():
                DG.add_node((i, j, k))

            # rotation edges
            DG.add_edge((i, j, ">"), (i, j, "v"), weight=1000)
            DG.add_edge((i, j, "v"), (i, j, ">"), weight=1000)

            DG.add_edge((i, j, "v"), (i, j, "<"), weight=1000)
            DG.add_edge((i, j, "<"), (i, j, "v"), weight=1000)

            DG.add_edge((i, j, "<"), (i, j, "^"), weight=1000)
            DG.add_edge((i, j, "^"), (i, j, "<"), weight=1000)

            DG.add_edge((i, j, "^"), (i, j, ">"), weight=1000)
            DG.add_edge((i, j, ">"), (i, j, "^"), weight=1000)


# build grap
for i in range(len(maze)):
    for j in range(len(maze[0])):
        for k, (dx, dy) in dirs.items():
            i_next, j_next = i + dx, j + dy

            if maze[i][j] == "#" or maze[i_next][j_next] == "#":
                continue

            if maze[i_next][j_next] == "E":
                target = (i_next, j_next)
            else:
                target = (i_next, j_next, k)

            DG.add_edge((i, j, k), target, weight=1)


print_maze()

score = nx.shortest_path_length(DG, source=(*pos_start, ">"), target=pos_end, weight="weight")
print(f"1) score is {score}")

nodes = set()

# NOTE: use a directed graph here so we have less cycles
for i, path in enumerate(
    nx.all_shortest_paths(DG, source=(*pos_start, ">"), target=pos_end, weight="weight")
):
    for node in path:
        nodes.add((node[0], node[1]))


print(f"2) unique tiles of paths are {len(nodes)}")
