import os

__DIR__ = os.path.dirname(os.path.abspath(__file__))

filename = "input.txt"

# try to fit X presents into the region, check yes/no
regions: list[tuple[tuple[int, int], list[int]]] = []
boxes: dict[int, int] = {}


with open(os.path.join(__DIR__, filename), "r") as f:
    lines = f.readlines()

    box_number, box_area = None, 0
    for line in lines:
        line = line.strip()

        if not line and box_number is not None:
            boxes[box_number] = box_area
            box_number, box_area = None, 0

        elif line.endswith(":"):
            box_number = int(line[:-1])

        elif "x" in line:
            region_str, fit_str = line.split(": ")
            regions.append((
                (int(region_str.split("x")[0]), int(region_str.split("x")[1])),
                [int(x) for x in fit_str.split(" ")],
            ))
        else:
            box_area += line.count("#")


def print_box(box: list[list[str]]):
    for row in box:
        print("".join(row))


result = 0

# NOTE: didn't write a packing algorithm with all the flips and rotations, seemed to be enough to check the constraints
for (region_x, region_y), counts in regions:
    total_box_area = 0

    for box_area, c in zip(boxes.values(), counts):
        total_box_area += box_area * c

    # 1. we need have have enough area overall
    if total_box_area <= region_x * region_y:
        # 2. all presents are 3x3, so we need to check if overall we can fit N packages
        if (region_x // 3) * (region_y // 3) >= sum(counts):
            result += 1


print(f"{result}")
