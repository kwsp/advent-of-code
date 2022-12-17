with open("day08.txt") as fp:
    s = fp.read()

grid = [[int(c) for c in l] for l in s.strip().split("\n")]


def part1(grid: list[list[int]]):
    visible = set()
    D1, D2 = len(grid), len(grid[0])

    # check rows
    for i, row in enumerate(grid):
        # check rows left to right
        row_max = -1
        for j, c in enumerate(row):
            if c > row_max:
                row_max = c
                visible.add((i, j))

        # check rows right to left
        row_max = -1
        for j in range(D2 - 1, -1, -1):
            c = row[j]
            if c > row_max:
                row_max = c
                visible.add((i, j))

    # check cols
    for j in range(D2):
        col = [row[j] for row in grid]

        col_max = -1
        # check col top to bottom
        for i, c in enumerate(col):
            c = col[i]
            if c > col_max:
                col_max = c
                visible.add((i, j))

        # check col bottom to top
        col_max = -1
        for i in range(D1 - 1, -1, -1):
            c = col[i]
            if c > col_max:
                col_max = c
                visible.add((i, j))

    # Viz
    # _viz = [[0 for _ in range(D2)] for _ in range(D1)]
    # for i, j in visible:
    # _viz[i][j] = 1
    # from pprint import pprint
    # pprint(_viz)

    return len(visible)


print("Part 1:", part1(grid))


def check_(val: int, lst: list[int]) -> int:
    try:
        tmp = next(i for i, x in enumerate(lst) if x >= val)
        if tmp == 0:
            return 1
        return tmp + 1
    except StopIteration:
        return len(lst)


assert check_(5, [5, 2]) == 1
assert check_(5, [3]) == 1
assert check_(5, [1, 2]) == 2
assert check_(5, [3, 5, 3]) == 2


def part2(grid: list[list[int]]):
    D1, D2 = len(grid), len(grid[0])

    row_lr = [[1 for _ in range(D2)] for _ in range(D1)]
    row_rl = [[1 for _ in range(D2)] for _ in range(D1)]

    col_tb = [[1 for _ in range(D2)] for _ in range(D1)]
    col_bt = [[1 for _ in range(D2)] for _ in range(D1)]

    # check rows
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            # check rows left to right
            row_lr[i][j] = check_(c, list(reversed(row[:j])))

            # check rows right to left
            row_rl[i][j] = check_(c, row[j + 1 :])

    # check cols
    for j in range(D2):
        col = [row[j] for row in grid]

        for i, c in enumerate(col):
            # check col top to bottom
            col_tb[i][j] = check_(c, list(reversed(col[:i])))

            # check col bottom to top
            col_bt[i][j] = check_(c, col[i + 1 :])

    scores = [
        [row_lr[i][j] * row_rl[i][j] * col_tb[i][j] * col_bt[i][j] for j in range(D2)]
        for i in range(D1)
    ]

    return max(max(l) for l in scores)


print("Part 2:", part2(grid))
