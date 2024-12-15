import os

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
            for j, element in enumerate(list(line)):
                if element == "@":
                    pos = (i, j)
            warehouse.append(list(line))
        else:
            moves += list(line)


def print_warehouse():
    for row in warehouse:
        print("".join(row))


dirs = {
    ">": (0, 1),
    "<": (0, -1),
    "^": (-1, 0),
    "v": (1, 0),
}


print_warehouse()
print(pos)


def push(i, j, dir):
    global pos
    i_iter, j_iter = i, j

    # find row of boxes
    while warehouse[i_iter][j_iter] == "O":
        i_iter += dir[0]
        j_iter += dir[1]

    # NO MOVE;
    if warehouse[i_iter][j_iter] == "#":
        return False

    if warehouse[i_iter][j_iter] == ".":
        warehouse[pos[0]][pos[1]] = "."
        pos = (i, j)
        warehouse[pos[0]][pos[1]] = "@"
        warehouse[i_iter][j_iter] = "O"
        return True

    raise ValueError("HUH?")


for move in moves:
    dir = dirs[move]
    i_next, j_next = pos[0] + dir[0], pos[1] + dir[1]

    if warehouse[i_next][j_next] == "#":
        continue
    elif warehouse[i_next][j_next] == ".":
        warehouse[pos[0]][pos[1]] = "."
        pos = (i_next, j_next)
        warehouse[pos[0]][pos[1]] = "@"

    elif warehouse[i_next][j_next] == "O":
        push(i_next, j_next, dir)


result = 0

for i in range(len(warehouse)):
    for j in range(len(warehouse[0])):
        element = warehouse[i][j]
        if element == "O":
            result += 100 * i + j


print_warehouse()

print(f"Result is: {result}")
