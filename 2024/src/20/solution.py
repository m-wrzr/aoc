import os
from typing import Counter

import networkx as nx

__DIR__ = os.path.dirname(os.path.abspath(__file__))

filename = "input.large.txt"

DG = nx.DiGraph()
matrix = []
start = end = (0, 0)

with open(os.path.join(__DIR__, filename), "r") as f:
    for i, line in enumerate(f.readlines()):
        matrix.append([])
        for j, c in enumerate(line.strip()):
            matrix[i].append(c)

            if c == "#":
                continue

            DG.add_node((i, j), value=c)

            if c == "S":
                start = (i, j)
            if c == "E":
                end = (i, j)


dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

cheating_edges = []

for i in range(len(matrix)):
    for j in range(len(matrix[i])):
        for d in dirs:
            i_new, y_new = i + d[0], j + d[1]
            if i_new < 0 or i_new >= len(matrix) or y_new < 0 or y_new >= len(matrix[i]):
                continue

            if matrix[i_new][y_new] != "#" and matrix[i][j] != "#":
                DG.add_edge((i, j), (i_new, y_new))

            # won't help to cheat into walls
            elif i != 0 and i != len(matrix) - 1 and j != 0 and j != len(matrix[i]) - 1:
                cheating_edges.append(((i, j), (i_new, y_new)))


def get_length(G: nx.Graph, start, end) -> int:
    return len(nx.shortest_path(G, start, end)) - 1


ct = Counter()

baseline = get_length(DG, start, end)

for i, (source, target) in enumerate(cheating_edges):
    print(f"Edge {i}/{len(cheating_edges)}")
    # only remove cheating edges
    if matrix[source[0]][source[1]] != "#" and matrix[target[0]][target[1]] == "#":
        di, dj = target[0] - source[0], target[1] - source[1]
        DG.add_edge(source, target)
        DG.add_edge(target, (target[0] + di, target[1] + dj))
        try:
            result = baseline - get_length(DG, start, end)
            if result >= 100:
                ct[result] += 1
                print(source, target, result)
        finally:
            DG.remove_edge(source, target)
            DG.remove_edge(target, (target[0] + di, target[1] + dj))

# NOTE: this only contains the solution for 1)
print(ct)
print(sum(ct.values()))
