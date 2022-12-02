from functools import reduce


def get_inp(fname="day09.txt"):
    with open(fname) as fp:
        lines = fp.read().strip().split("\n")
    return [[int(c) for c in line] for line in lines]


def is_low_pt(arr, i, j) -> bool:
    bottom = arr[i][j] < arr[i + 1][j] if i < len(arr) - 1 else True
    top = arr[i][j] < arr[i - 1][j] if i > 0 else True
    left = arr[i][j] < arr[i][j - 1] if j > 0 else True
    right = arr[i][j] < arr[i][j + 1] if j < len(arr[0]) - 1 else True
    return bottom and top and left and right


def get_low_pts(a):
    low_pts = []
    for i, row in enumerate(a):
        for j, v in enumerate(row):
            if is_low_pt(a, i, j):
                low_pts.append((v, (i, j)))
    return low_pts


def trace_low(arr, i, j, seen) -> int:
    if (
        i >= len(arr)
        or i < 0
        or j < 0
        or j >= len(arr[0])
        or arr[i][j] == 9
        or seen[i][j]
    ):
        return 0
    seen[i][j] = True

    bottom = (
        trace_low(arr, i + 1, j, seen)
        if i < len(arr) - 1 and arr[i][j] < arr[i + 1][j]
        else 0
    )
    top = trace_low(arr, i - 1, j, seen) if i > 0 and arr[i][j] < arr[i - 1][j] else 0
    left = trace_low(arr, i, j - 1, seen) if j > 0 and arr[i][j] < arr[i][j - 1] else 0
    right = (
        trace_low(arr, i, j + 1, seen)
        if j < len(arr[0]) - 1 and arr[i][j] < arr[i][j + 1]
        else 0
    )
    return bottom + top + left + right + 1


def part2():
    a = get_inp()
    low_pts = get_low_pts(a)
    seen = [[False] * len(a[0]) for _ in range(len(a))]
    basins = sorted([trace_low(a, i, j, seen) for _, (i, j) in low_pts])
    print("Part 2:", reduce(lambda acc, x: acc * x, basins[-3:], 1))


def part1():
    a = get_inp()
    low_pts = get_low_pts(a)
    print("Part 1:", sum(v + 1 for v, _ in low_pts))


part1()
part2()
