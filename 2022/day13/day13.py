with open("./day13.txt") as fp:
    s = fp.read()

inp = [tuple(eval(l) for l in pp.split("\n")) for pp in s.strip().split("\n\n")]


from enum import IntEnum


class CMP(IntEnum):
    LT = -1
    EQ = 0
    GT = 1


def _cmp(left, right) -> CMP:
    left_l = isinstance(left, list)
    right_l = isinstance(right, list)

    if left_l and right_l:
        for l, r in zip(left, right):
            res = _cmp(l, r)
            if res == CMP.EQ:
                continue
            return res
        return _cmp(len(left), len(right))

    if not left_l and not right_l:
        try:
            return CMP.LT if left < right else CMP.GT if left > right else CMP.EQ
        except:
            breakpoint()

    return _cmp(left, [right]) if left_l else _cmp([left], right)


def cmp(left, right):
    return _cmp(left, right) == CMP.LT


assert cmp([1, 1, 3, 1, 1], [1, 1, 5, 1, 1])
assert cmp([[1], [2, 3, 4]], [[1], 4])
assert not cmp([9], [8, 7, 6])
assert cmp([[4, 4], 4, 4], [[4, 4], 4, 4, 4])
assert not cmp([7, 7, 7, 7], [7, 7, 7])
assert cmp([], [3])
assert not cmp([[[]]], [[]])
assert not cmp([1, [2, [3, [4, [5, 6, 7]]]], 8, 9], [1, [2, [3, [4, [5, 6, 0]]]], 8, 9])


def suml(v):
    if isinstance(v, list):
        return sum(suml(l) for l in v)
    return v


res = 0
for i, (left, right) in enumerate(inp, start=1):
    if cmp(left, right):
        res += i
print("Part 1:", res)

flat = [v for p in inp for v in p]
flat.extend([[[2]], [[6]]])

from functools import cmp_to_key

flat_sort = sorted(flat, key=cmp_to_key(_cmp))


def _find(it, x):
    return next(i for i, v in enumerate(it, start=1) if v == x)


print("Part 2:", _find(flat_sort, [[2]]) * _find(flat_sort, [[6]]))
