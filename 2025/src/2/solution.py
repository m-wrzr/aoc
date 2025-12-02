import os
import textwrap

__DIR__ = os.path.dirname(os.path.abspath(__file__))

filename = "input.txt"


product_ranges: list[tuple[int, int]] = []

with open(os.path.join(__DIR__, filename), "r") as f:
    li = f.readline().split(",")

    for l in li:
        a, b = l.split("-")
        product_ranges.append((int(a), int(b)))


def solve_1():

    invalid: list[int] = []

    for x_range in product_ranges:
        for x in range(x_range[0], x_range[1] + 1):
            x_str = str(x)
            if len(x_str) % 2 == 0:
                middle = int(len(x_str) / 2)
                if x_str[:middle] == x_str[middle:]:
                    print(x_str)
                    invalid.append(x)

    print(f"RESULT {sum(invalid)}")


def is_invalid(x: int) -> bool:
    x_str = str(x)

    # single digit can't repeat
    if len(x_str) == 1:
        return False

    for i in range(1, len(x_str) + 1):
        # check repeat of single character
        if i == 1:
            if all(x_str[0] == x for x in x_str):
                return True
            else:
                continue

        wrapped = set(textwrap.wrap(x_str, i))

        # only one unique part
        if len(wrapped) == 1:
            # entire string is made of the same part, we already checked 1,1,1, ... before
            if next(iter(wrapped)) == x_str:
                continue

            print(x_str)
            return True

    return False


def solve_2():
    invalid: list[int] = []

    for x_range in product_ranges:
        for x in range(x_range[0], x_range[1] + 1):
            if is_invalid(x):
                invalid.append(x)

    print(f"RESULT {sum(invalid)}")


solve_2()
