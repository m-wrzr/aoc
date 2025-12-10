import os

from scipy.optimize import linprog

__DIR__ = os.path.dirname(os.path.abspath(__file__))

filename = "input.txt"


machines: list[
    tuple[
        str,  # target
        list[list[int]],  # buttons
        tuple,  # joltages
    ]
] = []


with open(os.path.join(__DIR__, filename), "r") as f:
    for line in f.readlines():
        for t in ["(", ")", "[", "]", "{", "}"]:
            line = line.replace(t, "")

        line_split = line.split(" ")

        target = line_split[0]

        buttons = []
        for butt in line_split[1:-1]:
            buttons.append([int(x) for x in butt.split(",")])

        joltages = tuple([int(x) for x in line_split[-1].split(",")])

        machines.append((target, buttons, joltages))


def flip(state: str, button: list[int]) -> str:
    r = list(state)
    for i in button:
        match r[i]:
            case ".":
                r[i] = "#"
            case "#":
                r[i] = "."
    return "".join(r)


def solve_1():
    result = 0

    for target, buttons, _ in machines:
        i = 0
        off = "".join(["." for _ in range(len(target))])
        current = {off}

        while target not in current:
            next_iter = set()

            for c in current:
                for button in buttons:
                    next_iter.add(flip(c, button))

            current = next_iter
            i += 1

        result += i

    print(f"1) {result}")


solve_1()


def solve_2():
    result = 0

    for _, buttons, joltages in machines:
        # each button costs "1" to press
        coefficients = [1] * len(buttons)

        A_eq = []
        # e.g. {3, 5, 6} how often should the button be pressed
        for button_id, n_to_press in enumerate(joltages):
            # constraint: which button increases which joltage
            A_eq.append([button_id in b for b in buttons])

        # target value that we want to solve for
        b_eq = joltages

        result += int(
            linprog(
                coefficients,
                A_eq=A_eq,
                b_eq=b_eq,
                # full numbers only, no partial button presses
                integrality=True,
            ).fun
        )

    print(f"2) {result}")


solve_2()
