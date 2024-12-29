import os

__DIR__ = os.path.dirname(os.path.abspath(__file__))

filename = "input.large.txt"

# height, 0-9
# trail:
# as long as possible
# even/gradual uphill

# any path from any 0 to 9, exactly increases by 1
# overall score is the number of unique paths to 9

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


def walk(i: int, j: int, hm: list[list[int]], path: list) -> list[list[tuple[int, int]]]:
    field_current = hm[i][j]

    path.append((i, j))

    paths = []

    # check surrounding nodes
    for dir in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
        try:
            i_next, j_next = i - dir[0], j - dir[1]

            if not (i_next >= 0 and j_next >= 0 and i_next < N and j_next < M):
                continue

            field = hm[i_next][j_next]

            if field == field_current + 1:
                if field == 9:
                    # do not return, other paths directions could also have 9s
                    paths.append(path + [(i_next, j_next)])
                else:
                    for r in walk(i_next, j_next, hm, path):
                        paths.append(r)

        except IndexError:
            pass

    return paths


result = 0
for i, j in trailheads:
    print((i, j))

    # clear duplicates via set conversion
    s = set()
    for r in walk(i, j, height_map, []):
        s.add(tuple(r))

    print((i, j))
    result += len(s)

print(result)
