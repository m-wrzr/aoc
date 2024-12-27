import os
from itertools import product

__DIR__ = os.path.dirname(os.path.abspath(__file__))

filename = "input.large.txt"


# lock: top row ##
# keys: top row ..

inputs = []
data = []
keys_base, locks_base = [], []


with open(os.path.join(__DIR__, filename), "r") as f:
    for line in f.readlines():
        line = line.strip()

        if not line:
            if data[0][0] == "#":
                locks_base.append(data)
            else:
                keys_base.append(data)
            data = []
            continue

        data.append(line)

# read pins left to right, dicount base row


def to_pin_height(m: list[list[str]]) -> list[int]:
    heights: list[int] = []
    for j in range(len(m[0])):
        heights.append(-1)
        for i in range(len(m)):
            if m[i][j] == "#":
                heights[j] += 1

    return heights


keys = [to_pin_height(k) for k in keys_base]
locks = [to_pin_height(l) for l in locks_base]


def is_match(key: list[int], lock: list[int]) -> bool:
    return all([(a + b) < 6 for a, b in zip(key, lock)])


agg = 0
for k, l in list(product(keys, locks)):
    print(k, l)
    if is_match(k, l):
        agg += 1


print(f"1) {agg}")
