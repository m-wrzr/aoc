import functools
import os

import networkx as nx

__DIR__ = os.path.dirname(os.path.abspath(__file__))

filename = "input.txt"


G = nx.DiGraph()
G_plain = {}


with open(os.path.join(__DIR__, filename), "r") as f:
    for line in f.readlines():
        node_from, node_to_str = line.strip().split(":")
        nodes_to_all = node_to_str.strip().split(" ")
        G_plain[node_from] = nodes_to_all

        for node_to in nodes_to_all:
            G.add_edge(node_from, node_to)


def solve_1():
    print(f"1) {len(list(nx.all_simple_paths(G, 'you', 'out')))}")


solve_1()


@functools.cache
def count(node_from, node_to) -> int:

    if node_from == node_to:
        return 1

    result = 0

    for _next in G_plain.get(node_from, []):
        result += count(_next, node_to)

    return result


def solve_2():
    # svr -> dac -> fft -> out
    svr_dac = count("svr", "dac")
    dac_fft = count("dac", "fft")
    fft_out = count("fft", "out")
    result1 = svr_dac * dac_fft * fft_out

    # svr -> fft -> dac -> out
    svr_fft = count("svr", "fft")
    fft_dac = count("fft", "dac")
    dac_out = count("dac", "out")
    result2 = svr_fft * fft_dac * dac_out

    print(f"2) {result1 + result2}")


solve_2()
