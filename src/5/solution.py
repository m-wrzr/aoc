import os

__DIR__ = os.path.dirname(os.path.abspath(__file__))

filename = "input.large.txt"

is_before_dict: dict[int, list[int]] = {}
is_after_dict: dict[int, list[int]] = {}


updates = []

with open(os.path.join(__DIR__, filename), "r") as f:
    fst = True

    # each row is a report, each one contains n columns
    for li in f.readlines():
        li = li.strip()

        if not li:
            fst = False
            continue

        if fst:
            l, r = [int(x) for x in li.split("|")]
            is_after_dict[l] = is_after_dict.get(l, []) + [r]
            is_before_dict[r] = is_before_dict.get(r, []) + [l]
        else:
            data = [int(x.strip()) for x in li.split(",")]
            updates.append(data)

# X|Y
# X before Y

updates_correct = []

n = 0

for update in updates:
    print("-----")
    print(update)
    valid = True
    for i, page_number in enumerate(update):
        pages_before = set(update[:i])
        pages_after = set(update[i + 1 :] if i < len(update) - 1 else [])

        print(pages_before, page_number, pages_after)
        print("isbefore", is_before_dict.get(page_number, []))
        print("isafter", is_after_dict.get(page_number, []))

        # no overlap between before and what should come after
        if set(is_after_dict.get(page_number, [])).intersection(pages_before):
            print("NOT VALID is_after,", page_number)
            valid = False
            break

        if set(is_before_dict.get(page_number, [])).intersection(pages_after):
            print("NOT VALID is_before", page_number)

            valid = False
            break

    if valid:
        n += update[int(len(update) / 2)]
        print("is valid")

print(n)
