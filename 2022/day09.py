from __future__ import annotations
from typing import Iterable, NamedTuple
import copy


class Pos(NamedTuple):
    x: int = 0
    y: int = 0

    def __add__(self, o):
        if isinstance(o, int):
            return Pos(self.x + o, self.y + o)
        elif isinstance(o, (Pos, tuple)):
            return Pos(self.x + o[0], self.y + o[1])
        raise ValueError()

    def __sub__(self, o):
        if isinstance(o, int):
            return Pos(self.x - o, self.y - o)
        elif isinstance(o, (Pos, tuple)):
            return Pos(self.x - o[0], self.y - o[1])
        raise ValueError()

    def __abs__(self):
        return Pos(abs(self.x), abs(self.y))

    def max(self):
        return max(self.x, self.y)

    def follow(self, head: Pos):
        d = head - self
        ad = abs(d)
        if ad.x > 1 and ad.y > 1:
            return self + Pos(d.x // 2, d.y // 2)
        if ad.x > 1:
            return self + Pos(d.x // 2, d.y)
        if ad.y > 1:
            return self + Pos(d.x, d.y // 2)

        return copy.deepcopy(self)


class Grid:
    def __init__(
        self, xrange: tuple[int, int] = (-10, 10), yrange: tuple[int, int] = (-10, 10)
    ):
        xrng = range(xrange[0], xrange[1] + 1)
        yrng = range(yrange[0], yrange[1] + 1)
        self.mid = Pos(-xrange[0], yrange[1])
        self.xrng = xrng
        self.yrng = yrng
        self.grid = [["." for _ in xrng] for _ in yrng]

    def mark(self, l: Iterable[Pos], marker="#"):
        for p in l:
            # print(p, [self.mid - p.y, self.mid + p.x])
            self.grid[self.mid.y - p.y][self.mid.x + p.x] = marker

    def print(self):
        self.mark([Pos(0, 0)], "S")
        print("\n".join("".join(row) for row in self.grid))


def plot(visited: set):
    x_min, x_max, y_min, y_max = 0, 0, 0, 0
    for p in visited:
        x_min = min(x_min, p.x)
        x_max = max(x_max, p.x)
        y_min = min(y_min, p.y)
        y_max = max(y_max, p.y)
    grid = Grid((x_min, x_max), (y_min, y_max))
    grid.mark(visited)
    grid.print()


with open("./day09.txt") as fp:
    s = fp.read()

_step = {"U": (0, 1), "D": (0, -1), "L": (-1, 0), "R": (1, 0)}
pairs = [(d, int(s)) for d, s in (l.strip().split(" ") for l in s.strip().split("\n"))]

## Part 1
head = Pos()
tail = Pos()
visited: set[Pos] = set()
for d, n in pairs:
    step = _step[d]
    for _ in range(n):
        head += step
        tail = tail.follow(head)
        visited.add(tail)

print("Part 1:", len(visited))
# plot(visited)


def plot_rope(rope: list[Pos]):
    x_min, x_max, y_min, y_max = 0, 0, 0, 0
    for p in rope:
        x_min = min(x_min, p.x)
        x_max = max(x_max, p.x)
        y_min = min(y_min, p.y)
        y_max = max(y_max, p.y)
    grid = Grid((x_min, x_max), (y_min, y_max))
    grid.mark([rope[0]], "H")
    for i, p in enumerate(rope[1:], start=1):
        grid.mark([p], str(i))
    grid.print()
    print()


## Part 2
rope = [Pos() for _ in range(10)]
visited: set[Pos] = set()
for d, n in pairs:
    step = _step[d]
    for _ in range(n):
        new_rope = [rope[0] + step]
        for i in range(1, len(rope)):
            new_rope.append(rope[i].follow(new_rope[-1]))

        rope = new_rope
        visited.add(rope[-1])

print("Part 2:", len(visited))
# plot(visited)
# plot_rope(rope)
