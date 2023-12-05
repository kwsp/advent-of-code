with open("./day04.txt") as fp:
    lines = fp.read().strip().split("\n")


ap = [[[int(i) for i in p.split("-")] for p in l.split(",")] for l in lines]


def complete_overlap(p1, p2):
    r1 = range(p1[0], p1[1] + 1)
    r2 = range(p2[0], p2[1] + 1)
    return all(i in r1 for i in p2) or all(i in r2 for i in p1)


print("Part 1:", sum(complete_overlap(p1, p2) for p1, p2 in ap))


def any_overlap(p1, p2):
    r1 = range(p1[0], p1[1] + 1)
    r2 = range(p2[0], p2[1] + 1)
    return any([i in r1 for i in p2]) or any([i in r2 for i in p1])


print("Part 2:", sum([any_overlap(p1, p2) for p1, p2 in ap]))
