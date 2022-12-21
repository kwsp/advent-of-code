from itertools import cycle
import numpy as np

_shapes = [
    "####",
    ".#.\n###\n.#.",
    "..#\n..#\n###",
    "#\n#\n#\n#",
    "##\n##",
]


def parse_shape(shape):
    """
    Parse a string rep. of a shape into a list of 2D coordinates (y, x)
    """
    pts = []
    lines = shape.split("\n")
    for y, line in enumerate(reversed(lines)):
        for x, c in enumerate(line):
            if c == "#":
                pts.append((y, x))
    return np.array(pts)


shapes = [parse_shape(shape) for shape in _shapes]
shapes_total_max_height = sum([s[:, 0].max() + 1 for s in shapes])

N_ROCKS = 2022  # total no. of rocks dropped
# N_ROCKS = 1000000000000  # total no. of rocks dropped
max_height = N_ROCKS * shapes_total_max_height

# grid starts max_height tall, 7 wide
grid = np.zeros((max_height, 7), dtype=np.uint8)


def top_row(grid):
    n = np.argmax(grid.max(axis=1)[::-1])
    if n == 0:
        return 0
    return len(grid) - n


def print_grid(grid, shape=None):
    if shape is not None:
        grid = grid.copy()
        put_shape(grid, shape, 2)

    s = ""
    cc = (".", "#", "@")
    for row in reversed(grid[: top_row(grid)]):
        s += "|" + "".join([cc[i] for i in row]) + "|\n"

    print(s + "+-------+\n")


def put_shape(grid, shape, v=1):
    for y, x in shape:
        grid[y, x] = v


def test_collide(grid, shape):
    y, x = shape[:, 0], shape[:, 1]
    return np.any(x < 0) or np.any(x >= 7) or np.any(y < 0) or np.any(grid[y, x] > 0)


_jet_pat = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
with open("./day17.txt") as fp:
    _jet_pat = fp.read().strip()

# coordinates in [y, x]
_jp = lambda c: -1 if c == "<" else 1
JET_PAT = [_jp(c) for c in _jet_pat]


def drop_shape(jet_pats, grid: np.ndarray, shape: np.ndarray):
    shape = shape.copy()

    shape[:, 0] += top_row(grid) + 3
    shape[:, 1] += 2

    for jet in jet_pats:
        # Move by jet
        shape[:, 1] += jet
        if test_collide(grid, shape):
            # revert jet move
            shape[:, 1] -= jet

        # Move down
        shape[:, 0] -= 1
        if test_collide(grid, shape):
            shape[:, 0] += 1
            break

    put_shape(grid, shape)


from tqdm import tqdm

jet_pats = cycle(JET_PAT)
for i in tqdm(range(N_ROCKS)):
    drop_shape(jet_pats, grid, shapes[i % len(shapes)])

# print_grid(grid)
print("Part 1:", top_row(grid))
