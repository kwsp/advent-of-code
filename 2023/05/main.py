from __future__ import annotations
from typing import Iterable, NamedTuple


with open("./inp.txt", "r") as fp:
    lines = [line.rstrip("\n") for line in fp]

seeds = [int(i) for i in lines[0].split(": ")[1].split(" ")]


class Range(NamedTuple):
    sstart: int
    srange: range
    dstart: int
    n: int

    @classmethod
    def parse(cls, line: str) -> Range:
        dstart, sstart, n = (int(i) for i in line.split())
        srange = range(sstart, sstart + n)
        return Range(sstart, srange, dstart, n)


def parse_name(line: str):
    l = line.split(" ")[0].split("-")
    return l[0], l[2]


def group_lines(lines: list[str]) -> Iterable[list[str]]:
    group = []
    for line in lines:
        if line:
            group.append(line)
        else:
            # found new group
            yield group
            group = []
    yield group


almanac: dict[tuple[str, str], list[Range]] = {}
names: list[str] = []
ordered_ranges: list[list[Range]] = []
for group in group_lines(lines[2:]):
    name = parse_name(group[0])
    ranges = sorted([Range.parse(r) for r in group[1:]])
    almanac[name] = ranges
    names.append(name)
    ordered_ranges.append(ranges)


import bisect

ranges = almanac[name]


def query(sname: str, v: int, dname: str):
    ranges = almanac[(sname, dname)]
    return queryfast(ranges, v)

# def queryfast(ranges: list[Range], v: int):
    # for r in ranges:
        # if v in r.srange:
            # return r.dstart - r.sstart + v
    # return v

def queryfast(ranges: list[Range], v: int):
    i = bisect.bisect_left(ranges, (v,))
    search_slice = slice(max(0, i - 1), min(len(ranges), i + 1))
    for r in ranges[search_slice]:
        if v in r.srange:
            return r.dstart - r.sstart + v
    return v


assert query("seed", 79, "soil") == 81
assert query("seed", 14, "soil") == 14
assert query("seed", 55, "soil") == 57
assert query("seed", 13, "soil") == 13


from functools import cache
from pprint import pprint

@cache
def soil2location(v: int):
    for ranges in ordered_ranges:
        v = queryfast(ranges, v)
    return v


assert soil2location(79) == 82
assert soil2location(14) == 43
assert soil2location(55) == 86
assert soil2location(13) == 35

part1 = min(soil2location(s) for s in seeds)
print(f"{part1=}")

def seeds_p2(seeds: list[int]) -> Iterable[int]:
    for i in range(0, len(seeds), 2):
        start, n = seeds[i], seeds[i + 1]
        for j in range(start, start + n):
            yield j


from tqdm import tqdm

total = sum(seeds[1::2])
part2 = min(soil2location(s) for s in tqdm(seeds_p2(seeds), total=total, desc="Part 2"))
print(f"{part2=}")

# Performance was               ~40000it/s to 45000it/s
# New perf with binary search   ~210000it/s 
