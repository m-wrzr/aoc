import os

import numpy as np

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
        a = [int(x) for x in lines.pop(0)[9:].split(", ")]
        b = [int(x) for x in lines.pop(0)[9:].split(", ")]
        prize = [int(x) + 10000000000000 for x in lines.pop(0)[7:].split(", ")]

        lines.pop(0)
        print(len(lines))
        inputs.append((a, b, prize))

overall = 0


def solve():
    na, nb = np.linalg.solve(
        np.array(
            [
                [a[0], b[0]],
                [a[1], b[1]],
            ],
            dtype=np.float64,
        ),
        np.array(
            [prize[0], prize[1]],
            dtype=np.float64,
        ),
    )

    if (abs(na - round(na)) < 0.0001) and (abs(nb - round(nb)) < 0.0001):
        token_spent = round(na) * 3 + round(nb) * 1
        return round(token_spent)

    return None


for a, b, prize in inputs:
    print("searching prize")

    solution = solve()
    if solution:
        print(f"Found prize, tokens: {solution}")
        overall += solution


print(overall)
