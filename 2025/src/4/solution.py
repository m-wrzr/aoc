import os

__DIR__ = os.path.dirname(os.path.abspath(__file__))

filename = "input.txt"


grid: list[list[str]] = []

with open(os.path.join(__DIR__, filename), "r") as f:
    for line in f.readlines():
        grid.append(list(line.strip()))


def count_adjacent(x: int, y: int, t: str) -> int:
    count = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue

            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
                if grid[ny][nx] == t:
                    count += 1

    return count


def solve_1() -> None:
    pass

    result = 0

    print(len(grid), len(grid[0]))

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == "@" and count_adjacent(x, y, "@") < 4:
                print(f"({x},{y})", grid[y][x])
                result += 1

    print(result)


def count_total() -> int:
    return sum(row.count("@") for row in grid)


def solve_2() -> None:
    global grid
    result = 0

    grid_copy = [row.copy() for row in grid]

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == "@" and count_adjacent(x, y, "@") < 4:
                # print(f"({x},{y})", grid[y][x])
                result += 1
                grid_copy[y][x] = "."

    grid = grid_copy

    # for row in grid:
    #     print("".join(row))
    # print("-------")

    if result > 0:
        solve_2()


total_pre = count_total()
solve_2()
total_post = count_total()

print(f"Removed: {total_pre - total_post}")
