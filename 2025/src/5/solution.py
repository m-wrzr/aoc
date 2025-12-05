import os

__DIR__ = os.path.dirname(os.path.abspath(__file__))

filename = "input.txt"


id_fresh_ranges: list[tuple[int, int]] = []
ids_available: list[int] = []

with open(os.path.join(__DIR__, filename), "r") as f:
    lines = f.readlines()

    for i in range(len(lines)):
        line = lines[i].strip()

        if not line:
            break

        a, b = (int(x) for x in line.split("-"))
        id_fresh_ranges.append((a, b))

    for i in range(len(id_fresh_ranges) + 1, len(lines)):
        line = lines[i].strip()

        ids_available.append(int(line))


def solve_1():
    fresh_ids = []
    for pid in ids_available:
        for a, b in id_fresh_ranges:
            if a <= pid <= b:
                fresh_ids.append(pid)
                break

    print(f"1) {len(fresh_ids)}")


solve_1()


def solve_2(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    for i in range(len(ranges)):
        for j in range(len(ranges)):
            if i == j:
                continue

            a_1, b_1 = ranges[i]
            a_2, b_2 = ranges[j]

            # if they overlap, we merge both ranges together, continue with the new range list recursively
            if a_2 <= a_1 <= b_2 or a_2 <= b_1 <= b_2:
                a, b = min(a_1, a_2), max(b_1, b_2)
                ranges.remove((a_1, b_1))
                ranges.remove((a_2, b_2))
                ranges.append((a, b))
                return solve_2(ranges)

    return ranges


# count up left over (non-overlapping) ranges (3, 5) == 3, 4, 5
print(f"2) {sum([b - a + 1 for (a, b) in solve_2(id_fresh_ranges)])}")
