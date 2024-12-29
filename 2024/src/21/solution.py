import os
import random
import sys

__DIR__ = os.path.dirname(os.path.abspath(__file__))

filename = "input.large.txt"

codes = []

with open(os.path.join(__DIR__, filename), "r") as f:
    for line in f.readlines():
        codes.append(line.strip())


# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+

num_pad = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "0": (3, 1),
    "A": (3, 2),  # start
}

#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+

dir_pad = {
    "^": (0, 1),
    "A": (0, 2),  # start
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
}


# we always have manhattan distance


def dir_to_dir(code: str):
    pos = dir_pad["A"]

    code_dir = ""

    for c in code:
        pos_next = dir_pad[c]

        # e.g. 2-3 == -1
        i = pos[0] - pos_next[0]
        j = pos[1] - pos_next[1]

        def add_j():
            nonlocal i, j, pos, code_dir

            while j != 0:
                if j > 0:
                    j -= 1
                    code_dir += "<"
                    pos = (pos[0], pos[1] - 1)

                else:
                    j += 1
                    code_dir += ">"
                    pos = (pos[0], pos[1] + 1)

        def add_i():
            nonlocal i, j, pos, code_dir

            while i != 0:
                if i > 0:
                    i -= 1
                    code_dir += "^"
                    pos = (pos[0] - 1, pos[1])

                else:
                    i += 1
                    code_dir += "v"
                    pos = (pos[0] + 1, pos[1])

        while i != 0 or j != 0:
            if i != 0 and j != 0:
                if random.randint(1, 2) == 1:
                    add_i()
                else:
                    add_j()

            elif i != 0:
                add_i()
            else:
                add_j()

            if pos[0] == 0 and pos[1] == 0:
                raise Exception

        code_dir += "A"
        pos = pos_next

    return code_dir


def numeric_to_dir(code: str) -> str:
    pos = num_pad["A"]

    code_dir = ""

    for c in code:
        pos_next = num_pad[c]

        # e.g. 2-3 == -1
        i = pos[0] - pos_next[0]
        j = pos[1] - pos_next[1]

        def add_i():
            nonlocal i, code_dir, pos
            while i != 0:
                if i > 0:
                    i -= 1
                    code_dir += "^"
                    pos = (pos[0] - 1, pos[1])

                else:
                    i += 1
                    code_dir += "v"
                    pos = (pos[0] + 1, pos[1])

        def add_j():
            nonlocal j, code_dir, pos
            while j != 0:
                if j > 0:
                    j -= 1
                    code_dir += "<"
                    pos = (pos[0], pos[1] - 1)

                else:
                    j += 1
                    code_dir += ">"
                    pos = (pos[0], pos[1] + 1)

        while i != 0 or j != 0:
            if i != 0 and j != 0:
                if random.randint(1, 2) == 1:
                    add_i()
                else:
                    add_j()

            elif i != 0:
                add_i()
            else:
                add_j()

            if pos[0] == 3 and pos[1] == 0:
                raise Exception

        code_dir += "A"
        pos = pos_next

    return code_dir


results = []

# NOTE: this only solves 1) in a very inefficient way. probably should have used a recursive approach
#       where you only resolve one step at a time (with it's different ways to get from ">" to "^" for example).
#       maybe rewriting this later..
for code in codes:
    print(code)
    len_min = sys.maxsize
    for _ in range(10_000):
        try:
            code_num = numeric_to_dir(code)
            code_dir_1 = dir_to_dir(code_num)
            code_dir_2 = dir_to_dir(code_dir_1)
            len_min = min(len_min, len(code_dir_2))
        except Exception:
            pass

    results.append(int(code.replace("A", "")) * len_min)
    print(f"{len_min} * {int(code.replace('A', ''))}")
    print("----------")

print(sum(results))
