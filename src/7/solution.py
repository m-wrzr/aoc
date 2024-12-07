import itertools
import os

__DIR__ = os.path.dirname(os.path.abspath(__file__))

filename = "input.large.txt"

equations = []

with open(os.path.join(__DIR__, filename), "r") as f:
    # each row is a report, each one contains n columns
    for li in f.readlines():
        li = str(li).strip()

        if not li:
            continue

        left, right = li.split(":")
        equations.append((int(left), [int(x) for x in right[1:].split(" ")]))

overall = 0

for result, parts in equations:
    print(result, parts)

    # get all possible combinations of the operators, use list for mutability
    # NOTE: remove "|"" operator for solution 1
    products = [list(t) for t in itertools.product("+*|", repeat=len(parts) - 1)]

    for pro in products:
        aggregate = 0

        for i, part in enumerate(parts):
            if i == 0:
                aggregate = part
            else:
                match pro[i - 1]:
                    case "+":
                        aggregate = aggregate + part
                    case "*":
                        aggregate = aggregate * part
                    case "|":
                        aggregate = int(str(aggregate) + str(part))

        if aggregate == result:
            print("-> found solution")
            overall += aggregate
            break

print(f"Result: {overall}")
