from typing import NamedTuple
from collections import defaultdict


class Bag(NamedTuple):
    colour: str


def load_input(path):
    with open(path) as f:
        raw = f.read().strip()
    data = raw.split("\n")

    map1 = defaultdict(list)
    map2 = defaultdict(list)

    for d in data:
        col0, res = d.split("contain")
        col0 = col0[: col0.find(" bag")]
        for s in res.split(","):
            count, col = s.strip().split(maxsplit=1)
            try:
                cnt_clr = (int(count), col[: col.find(" bag")])
                map1[col0].append(cnt_clr)
                map2[cnt_clr[1]].append(col0)
            except ValueError:
                if not "no other bags" in s:
                    raise ValueError(f"Failed to parse line: {s}")

    return map1, map2


def solution_part_1(map2, clr):
    s = set()
    parents = map2[clr]
    s.update(parents)
    for parent in parents:
        s.update(solution_part_1(map2, parent))
    return s


def solution_part_2(map1, clr):
    count = 0
    for cnt, clr_child in map1[clr]:
        count += cnt + cnt * solution_part_2(map1, clr_child)
    return count


def sol_part_2(map1, clr):
    return sum(
        [cnt + cnt * solution_part_2(map1, clr_child) for cnt, clr_child in map1[clr]]
    )


if __name__ == "__main__":
    path = "./day07input.txt"

    map1, map2 = load_input(path)
    c = "shiny gold"
    res = solution_part_1(map2, c)
    print("Part 1: ", len(res))

    res = sol_part_2(map1, c)
    print("Part 2: ", res)
