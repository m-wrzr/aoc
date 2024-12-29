import os

__DIR__ = os.path.dirname(os.path.abspath(__file__))

filename = "input.txt"

a, b = [], []

with open(os.path.join(__DIR__, filename), "r") as f:
    for li in f.readlines():
        if not li:
            continue

        a.append(int(li.split()[0]))
        b.append(int(li.split()[1]))


def solve_1(a, b):
    a = sorted(a)
    b = sorted(b)

    dist = 0

    for i in range(len(a)):
        diff = abs(a[i] - b[i])
        dist += diff
        print(a[i], b[i], abs(a[i] - b[i]))

    print(f"result: {dist}")


def solve_2(a, b):
    amounts_b = {}
    for element in b:
        if element in amounts_b:
            amounts_b[element] += 1
        else:
            amounts_b[element] = 1

    sim_score = 0

    for element in a:
        sim_score += element * amounts_b.get(element, 0)

    print(sim_score)


# solve_1(a, b)
solve_2(a, b)
