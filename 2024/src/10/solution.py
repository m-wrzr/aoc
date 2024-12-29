import os

__DIR__ = os.path.dirname(os.path.abspath(__file__))

filename = "input.large.txt"


# height, 0-9
# trail:
# as long as possible
# even/gradual uphill

# any path from any 0 to 9, exactly increases by 1
# overall score of a path is how many 9s it touches


height_map = []
trailheads = []

with open(os.path.join(__DIR__, filename), "r") as f:
    for i, line in enumerate(f.readlines()):
        if not line:
            continue

        height_map.append([])

        for j, field in enumerate(line.strip()):
            field = int(field)

            height_map[i].append(field)

            if field == 0:
                trailheads.append((i, j))


N, M = len(height_map), len(height_map[0])


def walk(i: int, j: int, hm: list[list[int]]) -> set[tuple[int, int]]:
    field_current = hm[i][j]
    trailends = set()

    # check surrounding nodes
    for dir in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
        try:
            i_next, j_next = i - dir[0], j - dir[1]

            if not (i_next >= 0 and j_next >= 0 and i_next < N and j_next < M):
                continue

            field = hm[i_next][j_next]

            if field == field_current + 1:
                if field == 9:
                    trailends.add((i_next, j_next))
                else:
                    trailends.update(walk(i_next, j_next, hm))

        except IndexError:
            pass

    return trailends


print(height_map)
print(trailheads)
print("---")


result = 0
for i, j in trailheads:
    r = len(walk(i, j, height_map))
    print((i, j), r)
    result += r
print(result)
