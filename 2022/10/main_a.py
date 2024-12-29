# addx V takes two cycles to complete. After two cycles, the X register is increased by the value V. (V can be negative.)
# noop takes one cycle to complete. It has no other effect.

# one register, X, initialized to 1
# signal strength (the cycle number multiplied by the value of the X register)
# during the 20th cycle and every 40 cycles after that

cycle, X = 0, 1

result = 0


def cycle_input(input: str):
    global X

    match input:
        case "addx":
            pass
        case "noop":
            pass
        case _:
            X += int(input)


with open("input.txt") as f:
    while line := f.readline().strip():

        for l in line.split(" "):
            cycle += 1

            if (cycle - 20) % 40 == 0:
                result += cycle * X
                print(f"cycle {cycle} signal strength: {cycle  * X}, {X}")

            cycle_input(l)

print(result)
