import os

__DIR__ = os.path.dirname(os.path.abspath(__file__))

filename = "input.test.txt"


# 12345
# alternates between file / free / file / free
# size representation
# 0..111....22222

# 2333133121414131402
# 00...111...2...333.44.5555.6666.777.888899

matrix: list[list] = []

with open(os.path.join(__DIR__, filename), "r") as f:
    # each row is a report, each one contains n columns
    tokens = [int(x) for x in list(f.read().strip())]


print("".join([str(x) for x in tokens]))


def n_empty(rep: list[str]) -> int:
    return len([r for r in rep if rep == "."])


def find_free_index(rep: list[str]) -> int:
    for i, r in enumerate(rep):
        if r == ".":
            return i

    raise ValueError


new_rep, file_id = [], 0

for i, t in enumerate(tokens):
    is_file = i % 2 == 0

    if is_file:
        new_rep += [str(file_id)] * t
        file_id += 1
    else:
        new_rep += ["."] * t

i_allocate = len(new_rep) - 1
i_free = find_free_index(new_rep)


while i_allocate > i_free:
    if i_allocate != ".":
        new_rep[i_free] = new_rep[i_allocate]
        new_rep[i_allocate] = "."

        i_free = find_free_index(new_rep)

    i_allocate -= 1

    print(i_allocate, i_free)


agg = 0
for i, t in enumerate(new_rep):
    if t == ".":
        break

    agg += i * int(t)

print(agg)
