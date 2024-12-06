import os
from enum import StrEnum

__DIR__ = os.path.dirname(os.path.abspath(__file__))

filename = "input.large.txt"


maze: list[list[str]] = []


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

        maze.append(list(li))


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


def get_starting_position(maze: list[list[str]]) -> tuple[int, int]:
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] in Directions.__members__.values():
                return (i, j)

    raise ValueError("No starting position found")


current_position = get_starting_position(maze)


def is_out_of_bounds(maze: list[list[str]], position: tuple[int, int]) -> bool:
    i, j = position
    return i < 0 or j < 0 or i >= len(maze) or j >= len(maze[0])


def print_maze(maze: list[list[str]]):
    for row in maze:
        print("".join(row))


while True:
    print(current_position)

    i, j = i_next, j_next = current_position

    print(maze[i][j])

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
        break

    if maze[i_next][j_next] == "#":
        maze[i][j] = Directions(maze[i][j]).turn()

    # this covers empty tiles and X
    else:
        maze[i_next][j_next] = maze[i][j]
        maze[i][j] = "X"
        current_position = (i_next, j_next)


def count_visits(maze):
    n = 0
    for row in maze:
        for field in row:
            if field == "X":
                n += 1
    return n


print_maze(maze)
print(f"#visits: {count_visits(maze)}")
