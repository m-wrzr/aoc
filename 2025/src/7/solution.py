import os
from collections import defaultdict

import networkx as nx

__DIR__ = os.path.dirname(os.path.abspath(__file__))

filename = "input.txt"

# beam at S, moves downward, pass through ".", splitter "^"

grid: list[list[str]] = []
beams: set[tuple[int, int]] = set()


with open(os.path.join(__DIR__, filename), "r") as f:
    for y, line in enumerate(f.readlines()):
        grid.append([])

        for x, value in enumerate(line.strip()):
            if value == "S":
                beams.add((x, y))

            grid[y].append(value)


def print_grid(g: list[list[str]]):
    for line in g:
        print("".join(line))


leaves: set[tuple[int, int]] = set()


def solve_1(current_beams: set[tuple[int, int]]):
    result = 0

    while len(current_beams) > 0:
        next_beams: set[tuple[int, int]] = set()

        for x, y in current_beams:
            # move beam downwards
            y_d = y + 1

            # reached the bottom, previous one was leaf
            if y_d >= len(grid):
                leaves.add((x, y))
                continue

            match grid[y_d][x]:
                case ".":
                    grid[y_d][x] = "|"
                    next_beams.add((x, y_d))
                case "|":
                    pass
                case "^":
                    x_l, x_r = x - 1, x + 1

                    if x_l >= 0 and grid[y_d][x_l] == ".":
                        grid[y_d][x_l] = "|"
                        next_beams.add((x_l, y_d))

                    if x_r < len(grid[0]) and grid[y_d][x_r] == ".":
                        grid[y_d][x_r] = "|"
                        next_beams.add((x_r, y_d))

                    result += 1

                case _:
                    raise ValueError("Invalid grid item")

        current_beams = next_beams
        # print("---------------")
        # print(f"beams: {current_beams}")
        # print_grid(grid)

    print(f"1) {result}")


solve_1(beams)


############


root: tuple[int, int] = list(beams)[0]


def build_graph() -> nx.DiGraph:
    # NOTE: build new graph

    edges: list[tuple[tuple[int, int], tuple[int, int]]] = []

    for y, row in enumerate(grid):
        for x, value in enumerate(grid[y]):
            if value == "|" or value == "S":
                y_d = y + 1
                if not (0 <= y_d < len(grid)):
                    continue

                if grid[y_d][x] == "^":
                    for x_diff in (-1, 1):
                        x_d = x - x_diff

                        if 0 <= x_d < len(grid[y]):
                            if grid[y_d][x_d] == "|":
                                edges.append(((x, y), (x_d, y_d)))

                elif grid[y_d][x] == "|":
                    edges.append(((x, y), (x, y_d)))

    G = nx.DiGraph()
    G.add_edges_from(edges)
    return G


G = build_graph()


# TODO: optimize
def solve_2_slow():
    paths: set[frozenset] = set()

    for i, leaf in enumerate(leaves):
        print(f"Processing leaf {i + 1}/{len(leaves)}")
        # print(f"----{leaf}---")
        pp = nx.all_simple_paths(G, root, leaf)
        print(f"Found {len(list(pp))} paths")
        for p in pp:
            # print(p)
            paths.add(frozenset(p))

    print(f"2) {len(paths)}")


def solve_2():
    counter: defaultdict[tuple[int, int], int] = defaultdict(int)
    counter[root] = 1

    # sort nodes by y, we can make sure we process parents before children
    sorted_nodes = sorted(G.nodes(), key=lambda n: n[1])

    for node in sorted_nodes:
        if node == root:
            continue

        # path to node == number of predecessors
        counter[node] = sum(counter[pred] for pred in G.predecessors(node))

    result = 0
    for leaf in leaves:
        result += counter[leaf]

    print(f"2) {result}")


# solve_2_slow()
solve_2()
