import os

__DIR__ = os.path.dirname(os.path.abspath(__file__))

filename = "input.large.txt"


A = 0
B = 0
C = 0


program: list[int] = []

with open(os.path.join(__DIR__, filename), "r") as f:
    for i, line in enumerate(f.readlines()):
        line = line.strip()
        if i == 0:
            A = int(line[11:])
        elif i == 1:
            B = int(line[11:])
        elif i == 2:
            Cs = int(line[11:])

        elif line:
            program = [int(x) for x in line[9:].split(",")]


def check_program(a: int) -> list[int]:
    print("checking ", a)
    out = []
    instruction_pointer = 0
    b = B
    c = Cs

    def get_combo_value(x: int) -> int:
        match x:
            case 0 | 1 | 2 | 3:
                return x
            case 4:
                return a
            case 5:
                return b
            case 6:
                return c
            # unused
            case 7:
                return -1
            case _:
                raise Exception(x)

    while instruction_pointer < len(program):
        opcode = program[instruction_pointer]
        literal = program[instruction_pointer + 1]
        combo = get_combo_value(literal)

        inc = 2

        match opcode:
            case 0:
                a = int(a / (2**combo))
            case 1:
                b = b ^ literal
            case 2:
                b = combo % 8
            case 3:
                if a != 0:
                    instruction_pointer = literal
                    inc = 0
            case 4:
                b = b ^ c
            case 5:
                new = combo % 8
                out.append(new)

            case 6:
                b = int(a / (2**combo))
            case 7:
                c = int(a / (2**combo))
            case _:
                raise Exception

        instruction_pointer += inc

    return out


# for 1)
print(check_program(A))


def backtrack(a_start: int, depth):
    if depth < 0:
        return a_start

    print(a_start)

    for i in range(8):
        a_next = a_start * 8 + i

        p = check_program(a_next)

        # go trough list from the back, last element should match first
        if p[0] == program[depth]:
            print(p)
            r_next = backtrack(a_next, depth - 1)
            if r_next:
                return r_next


# for 2)
print(backtrack(0, len(program) - 1))
