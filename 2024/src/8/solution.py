import itertools
import os

__DIR__ = os.path.dirname(os.path.abspath(__file__))

filename = "input.large.txt"

nodes: dict[str, list[tuple[int, int]]] = {}


matrix: list[list] = []

with open(os.path.join(__DIR__, filename), "r") as f:
    # each row is a report, each one contains n columns
    lines = f.readlines()

    M = len(lines[0].strip())
    N = len(lines)

    for i, li in enumerate(lines):
        li = list(str(li).strip())

        matrix.append([])

        for j, field in enumerate(li):
            matrix[i].append(field)
            if field != ".":
                nodes[field] = nodes.get(field, []) + [(i, j)]


combinations = {}
antinodes: set[tuple[int, int]] = set()

for k, v in nodes.items():
    combinations[k] = list(itertools.combinations(v, 2))


for k, v in combinations.items():
    print(f"Checking {k}")

    for fst, snd in v:
        i_diff, j_diff = fst[0] - snd[0], fst[1] - snd[1]

        def get_antinodes(i_diff, j_diff, fst, snd, iteration: int) -> set[tuple[int, int]]:
            # start at 0, appears on every antenna
            a1 = (fst[0] + i_diff * iteration, fst[1] + j_diff * iteration)
            a2 = (snd[0] - i_diff * iteration, snd[1] - j_diff * iteration)

            print("...", a1, a2)

            result = set()

            if a1[0] >= 0 and a1[0] < N and a1[1] >= 0 and a1[1] < M:
                result.add(a1)
            if a2[0] >= 0 and a2[0] < N and a2[1] >= 0 and a2[1] < M:
                result.add(a2)

            return result

        # for solution 1) start iteration at i==1 and add antinodes only once
        i = 0
        while True:
            result = get_antinodes(i_diff, j_diff, fst, snd, i)
            i += 1
            if not result:
                break
            else:
                antinodes.update(result)


# print nice matrix
for a in antinodes:
    matrix[a[0]][a[1]] = "#"

for row in matrix:
    print("".join(row))


print("-----")
print(f"Result is: {len(antinodes)}")

# antinode can be over antenna
# it's based on the position of
