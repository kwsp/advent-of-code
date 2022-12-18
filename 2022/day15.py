with open("./day15.txt") as fp:
    s = fp.read()

import re
from tqdm import tqdm
from numba import njit
from numba.typed import List


@njit()
def dist(s, b):
    return abs(s[0] - b[0]) + abs(s[1] - b[1])


Pair = tuple[int, int]


@njit()
def is_empty(pos: Pair, inp):
    """
    Check if a pos cannot contain a beacon
    """
    for s, b, d in inp:
        if dist(s, pos) <= d and pos != s and pos != b:
            return True
    return False


r = re.compile(r"x=(-?\d+), y=(-?\d+)")
pair2int = lambda p: (int(p[0]), int(p[1]))
sb2sbd = lambda pp: (pp[0], pp[1], dist(pp[0], pp[1]))
inp: list[tuple[Pair, Pair, int]] = List(
    [
        sb2sbd((pair2int(s), pair2int(b)))
        for s, b in (r.findall(l) for l in s.strip().split("\n"))
    ]
)


x_max, y_max = 0, 0
x_min, y_min = 0, 0
for s, b, d in inp:
    x_max = max(x_max, s[0] + d)
    y_max = max(y_max, s[1] + d)
    x_min = min(x_min, s[0] - d)
    y_min = min(y_min, s[1] - d)


part1 = sum(is_empty((x, 2000000), inp) for x in tqdm(range(x_min, x_max + 1)))
print("Part 1:", part1)


@njit()
def irange(start, stop):
    return range(start, stop + 1)


@njit()
def _part2(y, inp):
    x_ranges = []
    for s, _, d in inp:
        dx = d - abs(s[1] - y)
        if dx > 0:
            x_ranges.append((s[0] - dx, s[0] + dx))

    # reduce x_ranges
    x_ranges.sort()

    x_ranges_reduced = []
    i = 0
    curr = [*x_ranges[0]]
    while i < len(x_ranges):
        if curr[1] >= x_ranges[i][1]:
            i += 1
        elif curr[1] in irange(*x_ranges[i]):
            curr[1] = x_ranges[i][1]
            i += 1
        else:
            x_ranges_reduced.append(curr)
            curr = [*x_ranges[i]]
            i += 1

    x_ranges_reduced.append(curr)
    return x_ranges_reduced


def part2(rg: int, inp):
    rg += 1
    for y in tqdm(range(rg)):
        x_ranges_reduced = _part2(y, inp)

        if len(x_ranges_reduced) > 1:
            return x_ranges_reduced[0][1] + 1, y

    return -1, -1


p2 = part2(4000000, inp)
print("Part 2:", p2[0] * 4000000 + p2[1])
