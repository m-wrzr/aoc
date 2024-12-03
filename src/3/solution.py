import os
import re

__DIR__ = os.path.dirname(os.path.abspath(__file__))

filename = "input.large.txt"

rows = []

with open(os.path.join(__DIR__, filename), "r") as f:
    # each row is a report, each one contains n columns
    for li in f.readlines():
        if not li:
            continue

        rows.append(li)


pattern = r"mul\([0-9]+,[0-9]+\)|do\(\)|don't\(\)"

agg = 0

row = "".join(rows)
enabled = True

for match in re.finditer(pattern, row):
    g = match.group(0)

    print(g)

    if g == "do()":
        enabled = True
    elif g == "don't()":
        enabled = False
    elif enabled:
        l, r = [int(x) for x in g[4:-1].split(",")]
        agg += l * r

print(agg)
