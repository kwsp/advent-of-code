from collections import Counter, defaultdict
from typing import List
import math


with open("day14.txt") as fp:
    _base, _mp = fp.read().strip().split("\n\n")

base = list(_base)
mp = dict([l.split(" -> ") for l in _mp.split("\n")])

curr = base


def step(curr: List[str]):
    new = []
    for i in range(len(curr) - 1):
        p = "".join(curr[i : i + 2])
        new.append(curr[i])
        new.append(mp[p])
    new.append(curr[-1])
    return new


def bruteforce(steps):
    curr = base.copy()
    for _ in range(steps):
        curr = step(curr)
    print("len", curr.__len__())
    c = Counter(curr)
    cnts = c.most_common()
    print(cnts[0][1] - cnts[-1][1])


def smarter_alg(n=10):
    curr = base.copy()
    pairs = defaultdict(int)
    for i in range(len(curr) - 1):
        pairs["".join(curr[i : i + 2])] += 1
    for _ in range(n):
        new_pairs = defaultdict(int)
        for pair, cnt in pairs.items():
            c = mp[pair]
            new_pairs[pair[0] + c] += cnt
            new_pairs[c + pair[1]] += cnt
        pairs = new_pairs

    counter = defaultdict(int)
    for pair, cnt in pairs.items():
        counter[pair[0]] += cnt
        counter[pair[1]] += cnt

    counts = [math.ceil(i / 2) for i in counter.values()]
    print(max(counts) - min(counts))


n = 40
# bruteforce(n)
smarter_alg(n)
