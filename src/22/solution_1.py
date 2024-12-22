import os

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


agg = 0

for i, secret in enumerate(secrets):
    value = secret
    for iter in range(2000):
        value = next_secret(value)

    agg += value

print(f"Result: {agg}")
