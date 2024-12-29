import copy
import os
import time

__DIR__ = os.path.dirname(os.path.abspath(__file__))

filename = "input.large.txt"


robots = []
warehouse = []
moves = []

flip = True


pos: tuple[int, int] = (0, 0)

with open(os.path.join(__DIR__, filename), "r") as f:
    for i, line in enumerate(f.readlines()):
        line = line.strip()

        if not line:
            flip = False
            continue

        if flip:
            line_new = ""
            for j, element in enumerate(list(line)):
                if element == "@":
                    line_new += "@."
                elif element == ".":
                    line_new += ".."
                elif element == "#":
                    line_new += "##"
                elif element == "O":
                    line_new += "[]"

            warehouse.append(list(line_new))
        else:
            moves += list(line)


for i in range(len(warehouse)):
    for j in range(len(warehouse[0])):
        if warehouse[i][j] == "@":
            pos = (i, j)


def print_warehouse(wh=None):
    w = wh or warehouse
    for row in w:
        print("".join(row))


dirs = {
    ">": (0, 1),
    "<": (0, -1),
    "^": (-1, 0),
    "v": (1, 0),
}


# NOTE: approach for horizontal moves is to find the next free "." (if present)
#       and move everything inbetween for one dir
def push_horizontal(i, j, dir):
    _, dy = dir
    global pos
    j_iter = j

    slice = ""

    # find row of boxes
    while warehouse[i][j_iter] in ["[", "]"]:
        slice += warehouse[i][j_iter]

        j_iter += dy

    if slice.startswith("]"):
        slice = slice[::-1]

    # NO MOVE;
    if warehouse[i][j_iter] == "#":
        return

    if warehouse[i][j_iter] == ".":
        j_min, j_max = min(j, j_iter), max(j, j_iter)

        if dy < 0:
            warehouse[i][j_min:j_max] = slice
        else:
            print("move right")
            warehouse[i][j_min + 1 : j_max + 1] = slice
        print("slice is", slice, j_min, j_max)

        # pos[0] always the same
        warehouse[i][pos[1]] = "."
        pos = (i, j)
        warehouse[i][pos[1]] = "@"
        return

    raise ValueError("HUH?")


# NOTE: approach for vertical moves is to build a second warehouse (copy) and
#       move boxes without consideration of the environment. in a later step
#       we check if the resulting new warehouse is valid (nothing moved in #, etc.)
#       this is computationally and memory-wise not optimal but works...
def push_vertical_copy(wh, i, j, dir):
    dx, dy = dir
    e = wh[i + dx][j + dy]

    if e == "@":
        raise RuntimeError

    if e == "#" or e == ".":
        pass

    if e == "[":
        push_vertical_copy(wh, i + dx, j + dy, dir)
        push_vertical_copy(wh, i + dx, j + dy + 1, dir)

    if e == "]":
        push_vertical_copy(wh, i + dx, j + dy, dir)
        push_vertical_copy(wh, i + dx, j + dy - 1, dir)

    wh[i + dx][j + dy] = warehouse[i][j]
    wh[i][j] = "."


def is_copy_valid(warehouse, warehouse_copy) -> bool:
    for _i in range(len(warehouse)):
        for _j in range(len(warehouse[0])):
            e_old = warehouse[_i][_j]
            e_new = warehouse_copy[_i][_j]

            if e_new in ["[", "]"] and e_old == "#":
                return False

            if e_new == "[" and warehouse_copy[_i][_j + 1] != "]":
                return False

            if e_new == "]" and warehouse_copy[_i][_j - 1] != "[":
                return False

    return True


def push_vertical(i, j, dir):
    global pos
    warehouse_copy = copy.deepcopy(warehouse)
    push_vertical_copy(warehouse_copy, i, j, dir)

    if is_copy_valid(warehouse, warehouse_copy):
        warehouse_copy[i + dir[0]][j + dir[1]] = "@"
        pos = (i + dir[0], j + dir[1])
        return warehouse_copy

    else:
        return warehouse


for ct, move in enumerate(moves):
    print(f"#{ct} - MOVE IS ", move)

    dir = dirs[move]
    i_next, j_next = pos[0] + dir[0], pos[1] + dir[1]

    if warehouse[i_next][j_next] == "#":
        pass
    elif warehouse[i_next][j_next] == ".":
        warehouse[pos[0]][pos[1]] = "."
        pos = (i_next, j_next)
        warehouse[pos[0]][pos[1]] = "@"

    elif warehouse[i_next][j_next] in ["[", "]"]:
        if dir[0] == 0:
            push_horizontal(i_next, j_next, dir)

        else:
            warehouse = push_vertical(pos[0], pos[1], dir)

    print_warehouse()
    print()
    print()
    print()
    time.sleep(0.02)


print("FINISHED ALL MOVES ...")

result = 0

for i in range(len(warehouse)):
    for j in range(len(warehouse[0])):
        element = warehouse[i][j]
        if element == "[":
            result += 100 * i + j


print_warehouse(warehouse)

print(f"Result is: {result}")
