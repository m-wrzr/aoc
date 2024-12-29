import os
import sys

__DIR__ = os.path.dirname(os.path.abspath(__file__))

filename = "input.large.txt"


garden: list[list[str]] = []


# A kostet 3 tokens
# B kostet 1 token

inputs = []


def repl(s: str) -> str:
    return s.replace("X", "").replace("Y", "").replace("=", "").replace("+", "")


with open(os.path.join(__DIR__, filename), "r") as f:
    lines = [repl(l.strip()) for l in f.readlines()]

    while lines:
        a = [int(x) for x in lines.pop(0)[9:].split(", ")] + [3]
        b = [int(x) for x in lines.pop(0)[9:].split(", ")] + [1]
        prize = [int(x) for x in lines.pop(0)[7:].split(", ")]

        lines.pop(0)
        print(len(lines))
        inputs.append((a, b, prize))

overall = 0

for a, b, prize in inputs:
    print("searching prize")

    solution = sys.maxsize

    for ia in range(101):
        for ib in range(101):
            if ia * a[0] + ib * b[0] == prize[0] and ia * a[1] + ib * b[1] == prize[1]:
                solution = min(ia * a[2] + ib * b[2], solution)

    if solution != sys.maxsize:
        print(f"Found prize, tokens: {solution}")
        overall += solution


print(overall)
