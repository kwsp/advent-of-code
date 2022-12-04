with open("./day03.txt", "r") as fp:
    s = fp.read()

def split(s: str):
    s = s.strip()
    n = len(s)
    assert n % 2 == 0
    n = n//2
    return s[:n], s[n:]

def priority(c: str) -> int:
    i = ord(c)
    if i in range(ord('a'), ord('z') + 1):
        return i - ord('a') + 1
    return i - ord('A') + 27



lines = [l for l in s.strip().split("\n")]
sacks = [split(l) for l in lines]
common = [set(c1).intersection(set(c2)) for c1, c2 in sacks]
sum_p = sum([sum([priority(c) for c in s]) for s in common])
print("Part 1:", sum_p)
_sacks = [set(l) for l in lines]

badge_types = []
for i in range(0, len(sacks), 3):
    sets = _sacks[i:i+3]
    _s = sets[0].intersection(sets[1])
    _s = _s.intersection(sets[2])
    assert len(_s) == 1
    badge_types.append(next(iter(_s)))
p2 = sum([priority(c) for c in badge_types])
print("Part 2:", p2)
