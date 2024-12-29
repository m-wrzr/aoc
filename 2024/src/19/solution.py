import os
from functools import cache

__DIR__ = os.path.dirname(os.path.abspath(__file__))

filename = "input.large.txt"

towels = []
patterns = []

with open(os.path.join(__DIR__, filename), "r") as f:
    towels = f.readline().strip().split(", ")
    f.readline()
    for line in f.readlines():
        patterns.append(line.strip())


@cache
def check(pt: str) -> int:
    if not pt:
        return 1

    ct = 0

    for towel in towels:
        if pt.startswith(towel):
            ct += check(pt[len(towel) :])

    return ct


possible: dict[str, int] = {}

for i, pattern in enumerate(patterns):
    print(f"Checking {i}/{len(patterns)}")
    result = check(pattern)
    if result:
        possible[pattern] = result


print(f"1) {len(possible.keys())}")
print(f"2) {sum(possible.values())}")
