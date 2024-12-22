import os
from collections import Counter

__DIR__ = os.path.dirname(os.path.abspath(__file__))

filename = "input.large.txt"

secrets = []

with open(os.path.join(__DIR__, filename), "r") as f:
    for line in f.readlines():
        secrets.append(int(line.strip()))


# secret * 64
# mix
# prine
# dvode secret by 32, round down
# mix
# prine
# secret * 2048
# mix
# prune

# mix == bitwise xor / value ^ secret
# prune == modulo / value % 16777216


def next_secret(value: int) -> int:
    value = value ^ (value * 64)
    value = value % 16777216

    value = value ^ (value // 32)
    value = value % 16777216

    value = value ^ (value * 2048)
    value = value % 16777216

    return value


result = Counter()

for i, secret in enumerate(secrets):
    print(f"#{i + 1}, secret {secret}")
    value = secret
    last_digit = secret % 10

    deltas = []

    seq_map = Counter()

    for iter in range(2000):
        value = next_secret(value)
        next_digit = value % 10

        last_diff = next_digit - last_digit
        last_digit = next_digit

        deltas.append(last_diff)

        if len(deltas) > 3:
            index = tuple(deltas[-4:])
            # only consider first result
            if index not in seq_map:
                seq_map[index] = next_digit

    result += seq_map


highest = ("", 0)

for k, v in result.items():
    if v > highest[1]:
        highest = (k, v)


print(highest)
