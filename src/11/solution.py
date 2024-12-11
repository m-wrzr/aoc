import os
from collections import Counter

__DIR__ = os.path.dirname(os.path.abspath(__file__))

filename = "input.large.txt"


# stone == 0 -> replace with 1
# even number of digits (1204) -> split in (12) (4) - no leading zeros
# if no rules apply -> replace with old*2024

stones: list[int] = []

with open(os.path.join(__DIR__, filename), "r") as f:
    stones = [int(s) for s in f.read().strip().split(" ")]


# main insight is that I don't actually care about the order.
# it doesn't matter if the stone is at position 1 and 7, just that it appears twice
def blink(stones: list[int]) -> list[int]:
    result = []

    for s in stones:
        if s == 0:
            result.append(1)
        elif len(str(s)) % 2 == 0:
            s = str(s)
            result.append(int(s[: int(len(s) / 2)]))
            result.append(int(s[int(len(s) / 2) :]))
        else:
            result.append(s * 2024)

    return result


ct: Counter[int] = Counter(stones)

# update for solution 1)
for i in range(75):
    result = Counter()

    for item, amount in ct.items():
        if item == 0:
            result[1] += amount
        elif len(str(item)) % 2 == 0:
            item = str(item)
            result[int(item[: int(len(item) / 2)])] += amount
            result[int(item[int(len(item) / 2) :])] += amount
        else:
            result[item * 2024] += amount

    ct = result
    print(i + 1, sum(ct.values()))
