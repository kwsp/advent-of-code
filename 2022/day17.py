from itertools import cycle
import numpy as np
from numba import jit
from numba.typed import List

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
                pts.append((y, x + 2))
    return np.array(pts).T


shapes = [parse_shape(shape) for shape in _shapes]
shapes_total_max_height = sum([s[0].max() + 1 for s in shapes])

# N_ROCKS = 2022  # total no. of rocks dropped
N_ROCKS = 1000000000000  # total no. of rocks dropped
# max_height = N_ROCKS * shapes_total_max_height

# grid starts max_height tall, 7 wide
# grid = np.zeros((max_height, 7), dtype=np.uint8)
grid = np.zeros((100, 7), dtype=np.uint8)


@jit
def top_row(grid):
    row_max = np.array([row.max() for row in grid])
    n = np.argmax(np.flip(row_max))
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


@jit
def put_shape(grid, shape, v=1):
    y, x = shape[0], shape[1]
    for i in range(len(y)):
        grid[y[i], x[i]] = v


@jit
def test_collide(grid, shape):
    y, x = shape[0], shape[1]
    if np.any(x < 0) or np.any(x >= 7):
        return True
    if np.any(y < 0):
        return True
    for i in range(len(y)):
        if grid[y[i], x[i]] > 0:
            return True

    return False


@jit
def test_collide_x(grid, shape):
    y, x = shape
    return np.any(x < 0) or np.any(x >= 7) or np.any(grid[y, x] > 0)


@jit
def test_collide_y(grid, shape):
    y, x = shape
    return np.any(y < 0) or np.any(grid[y, x] > 0)


_jet_pat = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
with open("./day17.txt") as fp:
    _jet_pat = fp.read().strip()

# coordinates in [y, x]
_jp = lambda c: -1 if c == "<" else 1
JET_PAT = [_jp(c) for c in _jet_pat]


@jit
def drop_shape(jet_pats, i, grid: np.ndarray, shape: np.ndarray) -> int:
    shape = shape.copy()
    y, x = shape
    y += top_row(grid) + 3

    while True:
        jet = jet_pats[i]
        i = (i + 1) % len(jet_pats)
        # Move by jet
        x += jet
        if test_collide(grid, shape):
            # revert jet move
            x -= jet

        # Move down
        y -= 1
        if test_collide(grid, shape):
            y += 1
            break

    put_shape(grid, shape)
    return i


from tqdm import tqdm


y_offset = 0
jet_pat = List(JET_PAT)
jet_i = 0
for i in tqdm(range(N_ROCKS)):
    jet_i = drop_shape(jet_pat, jet_i, grid, shapes[i % len(shapes)])

    if top_row(grid) > 90:
        grid[:50] = grid[50:]
        grid[50:] = 0
        y_offset += 50


# print_grid(grid)
print("Part 1:", y_offset + top_row(grid))
