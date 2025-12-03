import os

__DIR__ = os.path.dirname(os.path.abspath(__file__))

filename = "input.txt"


# lines of batteries 1-9
# turn on exactly two batteries, in order -> make largest


batteries: list[list[int]] = []

with open(os.path.join(__DIR__, filename), "r") as f:
    for line in f.readlines():
        batteries.append([int(b) for b in line.strip()])


def solve_1(battery: list[int]) -> int:

    max_i, max_j = 0, 1
    max_value = battery[max_i] * 10 + battery[max_j]

    for i in range(len(battery)):
        # early stop
        if battery[i] < battery[max_i]:
            continue

        for j in range(i + 1, len(battery)):
            value = battery[i] * 10 + battery[j]
            if value > max_value:
                # print(f"New max value {value} > {max_value}, ({i},{j})")
                max_i, max_j, max_value = i, j, value

    # print(f"Max {max_value} at ({max_i},{max_j})")
    return max_value


print(f"1) {sum([int(solve_1(b)) for b in batteries])}")


def solve_2(battery: list[int], size: int) -> str:

    if size == 0:
        return ""

    for search in range(9, 0, -1):
        try:
            # get index of largest number, always preferred, even if at a late position in the string
            max_i = battery.index(search)

            if len(battery[max_i:]) >= size:
                # print(f"Found max at {max_i}")
                return str(battery[max_i]) + solve_2(battery[max_i + 1 :], size - 1)

        except ValueError:
            continue

    raise ValueError("Invalid battery")


print(f"2) {sum([int(solve_2(b, 12)) for b in batteries])}")
