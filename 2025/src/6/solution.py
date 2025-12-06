import os

import numpy as np

__DIR__ = os.path.dirname(os.path.abspath(__file__))

filename = "input.txt"

problems: list[tuple[str, tuple[int, int]]] = []

with open(os.path.join(__DIR__, filename), "r") as f:
    lines = [l.replace("\n", "") for l in f.readlines()]
    symbols_line = lines.pop()

    symbol, i_from, i_to = "", 0, 0

    # read in input, symbols first and ranges
    for i in range(len(symbols_line)):
        if symbols_line[i] in ("*", "+"):
            i_to = i - 1

            if symbol:
                problems.append((symbol, (i_from, i_to)))

            symbol = symbols_line[i]
            i_from = i
        elif i == len(symbols_line) - 1:
            i_to = len(symbols_line)
            problems.append((symbol, (i_from, i_to)))


def solve_1():
    result: int = 0

    for symbol, (i_from, i_to) in problems:
        numbers: list[int] = []

        for line in lines:
            numbers.append(int(line[i_from:i_to]))

        match symbol:
            case "+":
                result += sum(numbers)
            case "*":
                result += int(np.prod(np.array(numbers)))

    print(f"1) {result}")


solve_1()


def solve_2():
    result = 0

    for symbol, (i_from, i_to) in problems:
        numbers_str: list[str] = ["" for _ in range(len(lines))]

        for line in lines:
            for i, txt in enumerate(line[i_from:i_to]):
                if txt and txt != " ":
                    numbers_str[i] += txt

        numbers = [int(x) for x in numbers_str if x]

        if not numbers_str:
            continue

        match symbol:
            case "+":
                result += sum(numbers)
            case "*":
                result += int(np.prod(np.array(numbers)))

    print(f"2) {result}")


solve_2()
