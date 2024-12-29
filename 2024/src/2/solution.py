import os
import sys
from typing import Literal

__DIR__ = os.path.dirname(os.path.abspath(__file__))

filename = "input.txt"

rows = []

with open(os.path.join(__DIR__, filename), "r") as f:
    # each row is a report, each one contains n columns
    for li in f.readlines():
        if not li:
            continue

        rows.append([int(i) for i in li.split(" ")])


def is_safe(levels: list[int]) -> bool:
    incs: list[Literal["asc", "desc"]] = []

    for i, level in enumerate(levels):
        before = None if i == 0 else levels[i - 1]
        after = None if i >= len(levels) - 1 else levels[i + 1]

        if before and abs(before - level) > 3:
            incs = []
            break

        if after and abs(level - after) > 3:
            incs = []
            break

        if (before or sys.maxsize) > level > (after or -1):
            incs.append("desc")
        elif (before or -1) < level < (after or sys.maxsize):
            incs.append("asc")
        else:
            incs = []
            break

    if len(set(incs)) == 1:
        return True
    else:
        return False


# all increasing or all decreasing
# two adjacent levels differ by: at least one and at most three
def solve(vary_levels: bool = False):
    n_safe = 0

    def check_levels(levels):
        for i in [None] + list(range(len(levels))):
            if i is None:
                if is_safe(levels):
                    return True

            elif vary_levels:
                if is_safe(levels[:i] + levels[i + 1 :]):
                    return True

        return False

    for levels in rows:
        if check_levels(levels):
            n_safe += 1

    print(n_safe)


solve()
solve(vary_levels=True)
