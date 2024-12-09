import os
import sys

__DIR__ = os.path.dirname(os.path.abspath(__file__))

filename = "input.large.txt"


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


def find_free_block(rep: list[str], block_size: int) -> int:
    for i in range(len(rep) - block_size):
        slice = rep[i : i + block_size]
        if all([x == "." for x in slice]):
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


def find_next_file(new_rep: list, max_i: int) -> tuple[int, int]:
    fid = None

    slice = []

    for i in reversed(range(len(new_rep[: max_i + 1]))):
        e = new_rep[i]

        if fid is None and e != ".":
            fid = e

        if fid is not None and e == fid:
            slice.append(i)
        # next element, no match anymore
        elif fid is not None:
            break

    if fid is None:
        raise ValueError

    # print(f"found fid {fid} slice: {slice}")

    return slice[-1], len(slice)


i_max = sys.maxsize

print(len(new_rep))

(i_allocate, i_size) = 1, 0  # find_next_file(new_rep, i_max)
i_free = 0  # find_free_block(new_rep, i_size)


while i_max >= 0:
    print(i_max)
    # print("".join(new_rep))

    try:
        i_allocate, i_size = find_next_file(new_rep, i_max)
        i_free = find_free_block(new_rep, i_size)

        if i_free < i_allocate:
            new_rep[i_free : i_free + i_size] = new_rep[i_allocate : i_allocate + i_size]
            new_rep[i_allocate : i_allocate + i_size] = ["."] * i_size

    except ValueError:
        pass
    finally:
        i_max = i_allocate - 1


agg = 0
for i, t in enumerate(new_rep):
    if t == ".":
        continue

    agg += i * int(t)

print(agg)
