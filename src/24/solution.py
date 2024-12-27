import os
from typing import Literal

__DIR__ = os.path.dirname(os.path.abspath(__file__))

filename = "input.large.txt"


# AND / OR / XOR
# output is determined once

fst = True


BOOL_INT = Literal[0, 1]
OPERATOR = Literal["AND", "OR", "XOR"]

states: dict[str, int] = {}

ops: list[tuple[str, str, str, OPERATOR]] = []

with open(os.path.join(__DIR__, filename), "r") as f:
    for line in f.readlines():
        line = line.strip()

        if not line:
            fst = False
            continue

        if fst:
            x, y = line.split(": ")
            states[x] = int(y)  # type:ignore
        else:
            x, gate_out = line.split(" -> ")
            gate_a, op, gate_b = x.split(" ")
            ops.append((gate_a, gate_b, gate_out, op))  # type: ignore


while ops:
    i_next = None

    for i, (gate_a, gate_b, _, _) in enumerate(ops):
        if gate_a in states and gate_b in states:
            i_next = i
            break

    if i_next is None:
        raise ValueError("Can't continue")

    gate_a, gate_b, gate_out, op = ops.pop(i_next)

    match op:
        case "AND":
            states[gate_out] = states[gate_a] and states[gate_b]
        case "OR":
            states[gate_out] = states[gate_a] or states[gate_b]
        case "XOR":
            states[gate_out] = states[gate_a] ^ states[gate_b]

# only 1) - neither time nor brain capacity
z_keys = sorted([s for s in states if s.startswith("z")])
z_vals = reversed([str(states[k]) for k in z_keys])
z_out = int("".join(z_vals), 2)
print(f"1) {z_out}")
