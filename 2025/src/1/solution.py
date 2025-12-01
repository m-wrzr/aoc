import os
from typing import Literal

__DIR__ = os.path.dirname(os.path.abspath(__file__))

filename = "input.txt"

# Lx / Ry
# numbers 0 -> 99 ordered
rows: list[tuple[Literal["L", "R"], int]] = []

with open(os.path.join(__DIR__, filename), "r") as f:
    for li in f.readlines():
        if not li:
            continue

        direction, steps = (li[0], int(li[1:]))
        if direction not in ("L", "R"):
            raise ValueError

        rows.append((direction, steps))

dial, password = 50, 0


def move_dial_1(direction: Literal["L", "R"], steps: int):
    global dial, password

    match direction:
        case "L":
            dial = (dial - steps) % 100
        case "R":
            dial = (dial + steps) % 100

    if dial == 0:
        password += 1


def move_dial_2(direction: Literal["L", "R"], steps: int):
    global dial, password

    # still linear, we're max N*100 steps
    match direction:
        case "L":
            for _ in range(steps):
                dial = (dial - 1) % 100
                if dial == 0:
                    password += 1

        case "R":
            for _ in range(steps):
                dial = (dial + 1) % 100
                if dial == 0:
                    password += 1


for i, row in enumerate(rows):
    move_dial_2(*row)


print(f"Password is: {password}")
