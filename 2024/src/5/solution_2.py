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


def check_is_valid(update) -> tuple[bool, set[frozenset[int]]]:
    valid = True

    switches = set()

    for i, page_number in enumerate(update):
        pages_before = set(update[:i])
        pages_after = set(update[i + 1 :] if i < len(update) - 1 else [])

        print("----")
        print(pages_before, page_number, pages_after)

        # no overlap between before and what should come after
        should_not_be_before_current = set(is_after_dict.get(page_number, [])).intersection(
            pages_before
        )

        if should_not_be_before_current:
            print("NOT VALID is_after,", page_number, should_not_be_before_current)

            for x in should_not_be_before_current:
                switches.add(frozenset((page_number, x)))

            valid = False

        should_not_be_after_current = set(is_before_dict.get(page_number, [])).intersection(
            pages_after
        )

        if should_not_be_after_current:
            print("NOT VALID is_before", page_number, should_not_be_after_current)

            for x in should_not_be_after_current:
                switches.add(frozenset((page_number, x)))

            valid = False

    return valid, switches


# change the places of two list items
# these are sets to avoid switching duplicates (probably unneeded since we apply one at a time)
def apply(update, switch: frozenset[int]) -> list[int]:
    l, r = list(switch)
    il = update.index(l)
    ir = update.index(r)

    tmp = update[il]
    update[il] = update[ir]
    update[ir] = tmp

    return update


for update in updates:
    print("-----")
    print("old-order", update)

    became_valid = False
    valid, switches = check_is_valid(update)

    # ignore already valid stuff
    if valid:
        continue

    # apply the a switching rule until we get a valid updates list
    while not became_valid:
        update = apply(update, list(switches)[0])
        valid, switches = check_is_valid(update)
        became_valid = valid

    print("new-order", update)
    n += update[int(len(update) / 2)]
    print("is valid")

print(n)
