import os
import re
import time
from collections import Counter

__DIR__ = os.path.dirname(os.path.abspath(__file__))

filename = "input.large.txt"


robots = []


X_MAX, Y_MAX = 101, 103
# X_MAX, Y_MAX = 11, 7

with open(os.path.join(__DIR__, filename), "r") as f:
    for line in f.readlines():
        px, py, vx, vy = [int(num) for num in re.findall(r"-?\d+", line)]
        robots.append(((px, py), (vx, vy)))


# x (from left wall) y (from top wall) .... inverted
# robot vector in tiles per second
# v=1,-2 means that each second, the robot moves 1 tile to the right and 2 tiles up


def get_grid() -> str:
    c = Counter()

    for (x, y), (_, _) in robots:
        c[(x, y)] += 1

    out = ""

    for y in range(Y_MAX):
        for x in range(X_MAX):
            if (x, y) in c:
                out += str(c[(x, y)])
            else:
                out += "."
        out += "\n"

    return out


def print_grid():
    lines = get_grid().split("\n")
    for line in lines:
        print(line)


# make this 100 for task 1)
for sec in range(100_000):
    for i in range(len(robots)):
        px, py = robots[i][0]
        vx, vy = robots[i][1]

        px = (px + vx) % X_MAX
        py = (py + vy) % Y_MAX

        robots[i] = ((px, py), robots[i][1])

    # approach was to just print the grind into a file and look for patterns
    # from visual output inspection: there is some sort of pattern each 101 (X_MAX) seconds, starting 67
    if not (((sec - 67) % 101) == 0):
        continue

    out = get_grid()

    with open("out.txt", "a") as f:
        f.write("\n\n\n\n\n")
        f.write(f"seconds: {sec}\n")

        for line in out.splitlines():
            f.write(line)
            f.write("\n")

    print("-----")

    time.sleep(1)

##### SOLUTION 1 ONLY ######


def get_quadrant(x: int, y: int) -> int | None:
    if x == int(X_MAX / 2) or y == int(Y_MAX / 2):
        return None

    if x < int(X_MAX / 2):
        if y < int(Y_MAX / 2):
            return 1
        else:
            return 3
    else:
        if y < int(Y_MAX / 2):
            return 2
        else:
            return 4


ct = Counter()


for (x, y), (_, _) in robots:
    q = get_quadrant(x, y)
    if q:
        ct[q] += 1

agg = 1
for v in ct.values():
    agg *= v


print_grid()
print(f"solution is {agg}")
