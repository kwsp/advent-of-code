with open("day17.txt") as fp:
    lines = fp.read().strip().split("\n")

N_CYCLES = 6
L = len(lines) + N_CYCLES * 3

mid = L // 2
start_i = mid - len(lines) // 2


def mk3d(L: int) -> list[list[list[int]]]:
    return [[[0 for _ in range(L)] for _ in range(L)] for _ in range(L)]


grid = mk3d(L)
for i, line in enumerate(lines):
    for j, c in enumerate(line):
        if c == "#":
            grid[start_i + i][start_i + j][mid] = 1


def count_active_neighbours_3d(grid, i, j, k) -> int:
    count = 0
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            for dz in range(-1, 2):
                if dx == dy == dz == 0:
                    continue
                count += grid[i + dx][j + dy][k + dz]
    return count


def one_cycle_3d(grid):
    gg = mk3d(L)
    for i in range(1, L - 1):
        for j in range(1, L - 1):
            for k in range(1, L - 1):
                c = count_active_neighbours_3d(grid, i, j, k)
                curr = grid[i][j][k]
                if curr and c in range(2, 4):
                    gg[i][j][k] = 1
                    continue
                if not curr and c == 3:
                    gg[i][j][k] = 1
                    continue
    return gg


def sum_grid(grid: list[list[list[int]]]) -> int:
    s = 0
    for i in range(L):
        for j in range(L):
            s += sum(grid[i][j])
    return s


gg = grid
for _ in range(N_CYCLES):
    gg = one_cycle_3d(gg)

print("Part 1:", sum_grid(gg))


def mk4d(L: int) -> list[list[list[list[int]]]]:
    return [
        [[[0 for _ in range(L)] for _ in range(L)] for _ in range(L)] for _ in range(L)
    ]


grid = mk4d(L)
for i, line in enumerate(lines):
    for j, c in enumerate(line):
        if c == "#":
            grid[start_i + i][start_i + j][mid][mid] = 1


def count_active_neighbours_4d(grid, i, j, k, l) -> int:
    count = 0
    for di in range(-1, 2):
        for dj in range(-1, 2):
            for dk in range(-1, 2):
                for dl in range(-1, 2):
                    if di == dj == dk == dl == 0:
                        continue
                    count += grid[i + di][j + dj][k + dk][l + dl]
    return count


def one_cycle_4d(grid):
    gg = mk4d(L)
    for i in range(1, L - 1):
        for j in range(1, L - 1):
            for k in range(1, L - 1):
                for l in range(1, L - 1):
                    c = count_active_neighbours_4d(grid, i, j, k, l)
                    curr = grid[i][j][k][l]
                    if curr and c in range(2, 4):
                        gg[i][j][k][l] = 1
                        continue
                    if not curr and c == 3:
                        gg[i][j][k][l] = 1
                        continue
    return gg


def sum_grid_4d(grid: list[list[list[list[int]]]]) -> int:
    s = 0
    for i in range(L):
        for j in range(L):
            for k in range(L):
                s += sum(grid[i][j][k])
    return s


from tqdm import tqdm

gg = grid
for _ in tqdm(range(N_CYCLES)):
    gg = one_cycle_4d(gg)

print("Part 2:", sum_grid_4d(gg))
