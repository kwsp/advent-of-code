from collections import defaultdict


with open("day12.txt") as fp:
    lines = fp.read().strip().split("\n")

caves = []
nodes = []
adj_l = defaultdict(list)
for line in lines:
    c1, c2 = line.split("-")
    adj_l[c1].append(c2)
    adj_l[c2].append(c1)


def search1(curr: str, targ: str, seen: set) -> int:
    if curr in seen:
        return 0
    if curr == targ:
        return 1
    if not curr.isupper():
        seen.add(curr)
    return sum(search1(node, targ, seen.copy()) for node in adj_l[curr])


def search2(curr: str, targ: str, path: list, used2: bool) -> int:
    if curr == targ:
        return 1
    if curr.islower():
        c = path.count(curr)
        if c >= 1 and (curr == "start" or used2):
            return 0
        if c == 1 and not used2:
            used2 = True

    path.append(curr)
    return sum(search2(node, targ, path.copy(), used2) for node in adj_l[curr])


def part1():
    return search1("start", "end", set())


print("Part 1:", part1())


def part2():
    return search2("start", "end", [], False)


print("Part 2:", part2())
