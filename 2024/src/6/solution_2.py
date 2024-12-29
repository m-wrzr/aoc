import copy
import os
from enum import StrEnum
from typing import Iterator

__DIR__ = os.path.dirname(os.path.abspath(__file__))

filename = "input.large.txt"


original_maze: list[list[str]] = []


# # obstruction ]]]†\\

# </>/^/v guard looking \

# guard goes forward until #, then turns right

with open(os.path.join(__DIR__, filename), "r") as f:
    fst = True

    # each row is a report, each one contains n columns
    for li in f.readlines():
        li = li.strip()

        if not li:
            continue

        original_maze.append(list(li))


class Directions(StrEnum):
    top = "^"
    left = "<"
    right = ">"
    bottom = "v"

    def turn(self):
        match self:
            case Directions.top:
                return Directions.right

            case Directions.right:
                return Directions.bottom

            case Directions.bottom:
                return Directions.left

            case Directions.left:
                return Directions.top

    def symbol(self):
        match self:
            case Directions.top:
                return "t"

            case Directions.right:
                return "r"

            case Directions.bottom:
                return "b"

            case Directions.left:
                return "l"


def get_starting_position(maze: list[list[str]]) -> tuple[int, int]:
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] in Directions.__members__.values():
                return (i, j)

    raise ValueError("No starting position found")


def is_out_of_bounds(maze: list[list[str]], position: tuple[int, int]) -> bool:
    i, j = position
    return i < 0 or j < 0 or i >= len(maze) or j >= len(maze[0])


def print_maze(maze: list[list[str]]):
    for row in maze:
        print("".join(row))


def get_modified_mazes(maze) -> Iterator[list[list[str]]]:
    for i, row in enumerate(maze):
        for j, field in enumerate(row):
            if field == ".":
                m_copy = copy.deepcopy(maze)
                m_copy[i][j] = "#"
                yield m_copy


# TODO: pass maze with modification
def check_maze(maze) -> bool:
    current_position = get_starting_position(maze)
    post_positions: set[tuple[int, int, str]] = set()

    while True:
        i, j = i_next, j_next = current_position
        t = (i, j, maze[i][j])

        # print(t)

        if t in post_positions:
            print("LOOOOOOP")
            return True
        else:
            post_positions.add(t)

        match maze[i][j]:
            case Directions.top:
                i_next -= 1
            case Directions.bottom:
                i_next += 1
            case Directions.left:
                j_next -= 1
            case Directions.right:
                j_next += 1
            case _:
                raise ValueError("Lost track of guard")

        if is_out_of_bounds(maze, (i_next, j_next)):
            maze[i][j] = "X"
            return False

        if maze[i_next][j_next] == "#":
            maze[i][j] = Directions(maze[i][j]).turn()

        # this covers empty tiles and X
        else:
            maze[i_next][j_next] = maze[i][j]
            maze[i][j] = "X"
            current_position = (i_next, j_next)


def get_visits(maze):
    positions = []
    for i, row in enumerate(maze):
        for j, field in enumerate(row):
            if field == "X":
                positions.append((i, j))

    return positions


n_looped = 0

for i, m in enumerate(get_modified_mazes(original_maze)):
    print(f"{i}")
    if check_maze(m):
        print("loop found")
        n_looped += 1

print(f"#visits: {n_looped}")
