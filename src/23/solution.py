import os

import networkx as nx

__DIR__ = os.path.dirname(os.path.abspath(__file__))

filename = "input.large.txt"

G = nx.Graph()

with open(os.path.join(__DIR__, filename), "r") as f:
    for line in f.readlines():
        G.add_edge(*line.strip().split("-"))


cliques = set()
max_clique = []

for clique in nx.enumerate_all_cliques(G):
    if len(clique) > len(max_clique):
        max_clique = clique

    if len(clique) != 3:
        continue

    if any(c.startswith("t") for c in clique):
        cliques.add(tuple(clique))


print(f"1) {len(cliques)}")
print(f"2) {','.join(sorted(max_clique))}")
