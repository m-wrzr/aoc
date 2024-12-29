import os

__DIR__ = os.path.dirname(os.path.abspath(__file__))

filename = "input.large.txt"

rows = []

with open(os.path.join(__DIR__, filename), "r") as f:
    # each row is a report, each one contains n columns
    for li in f.readlines():
        li = li.strip()

        if not li:
            continue

        rows.append(list(li))


# get all 4 length slices of the matrix


def is_xmas(chars: list[str]) -> bool:
    word = "".join(chars)
    word = word.lower()
    return word == "xmas" or word == "samx"


def solve_1():
    n = 0

    # horizontal
    for i in range(len(rows)):
        for j in range(len(rows[i]) - 3):
            if is_xmas(rows[i][j : j + 4]):
                n += 1

    # vertical
    for i in range(len(rows) - 3):
        for j in range(len(rows[i])):
            if is_xmas([rows[i + k][j] for k in range(4)]):
                n += 1

    print("------")

    # diagonal top left to bottom right
    for i in range(len(rows) - 3):
        for j in range(len(rows[i]) - 3):
            if is_xmas([rows[i + k][j + k] for k in range(4)]):
                n += 1

    # diagonal top right to bottom left
    for i in range(len(rows) - 3):
        for j in range(3, len(rows[i])):
            if is_xmas([rows[i + k][j - k] for k in range(4)]):
                n += 1

    print(n)


def solve_2():
    n = 0

    def is_x_mas(matrix: list[list[str]]):
        print(matrix)
        slice_1 = (matrix[0][0] + matrix[1][1] + matrix[2][2]).lower()
        slice_2 = (matrix[0][2] + matrix[1][1] + matrix[2][0]).lower()

        return (slice_1 == "mas" or slice_1 == "sam") and (slice_2 == "mas" or slice_2 == "sam")

    for i in range(1, len(rows) - 1):
        for j in range(1, len(rows[0]) - 1):
            matrix = [
                [rows[row][col] for col in range(j - 1, j + 2)] for row in range(i - 1, i + 2)
            ]

            if is_x_mas(matrix):
                n += 1

    print(n)


solve_2()
