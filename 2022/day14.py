with open("./day14.txt") as fp:
    s = fp.read()

inp = [
    [[int(i) for i in pair.split(",")] for pair in l.split(" -> ")]
    for l in s.strip().split("\n")
]


class P1:
    def __init__(self, inp):
        x_min = min(min(p[0] for p in l) for l in inp)
        x_max = max(max(p[0] for p in l) for l in inp)
        y_max = max(max(p[1] for p in l) for l in inp)
        x_range = x_max - x_min

        grid = [["." for _ in range(x_range + 1)] for _ in range(y_max + 1)]

        for l in inp:
            assert len(l) >= 2
            p1 = l[0]
            for p2 in l[1:]:
                if p1[0] == p2[0]:
                    x = p1[0]
                    p = p1[1], p2[1]
                    for y in range(min(p), max(p) + 1):
                        grid[y][x - x_min] = "#"
                else:
                    y = p1[1]
                    p = p1[0], p2[0]
                    for x in range(min(p), max(p) + 1):
                        grid[y][x - x_min] = "#"
                p1 = p2

        self.grid = grid
        self.x_min = x_min
        self.n_sand = 0

    def print_grid(self):
        for c in str(self.x_min):
            print(f"   {c}")
        print("\n".join((f"{i:2} " + "".join(l) for i, l in enumerate(self.grid))))

    def drop_sand(self, start_x=500):
        grid = self.grid
        x = start_x - self.x_min
        y = 0
        if self.grid[y][x] != ".":
            return False

        while True:
            # check fall through
            if y + 1 == len(grid):
                return False

            # try to move down
            if grid[y + 1][x] == ".":
                y += 1
                continue

            # try to move down left
            if grid[y + 1][x - 1] == ".":
                y += 1
                x -= 1
                continue

            # try to move down right
            if grid[y + 1][x + 1] == ".":
                y += 1
                x += 1
                continue

            # cannot move
            break

        grid[y][x] = "o"
        self.n_sand += 1
        return True


p1 = P1(inp)
while p1.drop_sand():
    ...

# p1.print_grid()
print("Part 1:", p1.n_sand)


class P2(P1):
    def __init__(self, inp):
        super().__init__(inp)
        X = len(self.grid[0])
        self.grid.append(["." for _ in range(X)])
        self.grid.append(["#" for _ in range(X)])

    def expand_left(self):
        self.grid = [["."] + l for l in self.grid]
        self.grid[-1][0] = "#"
        self.x_min -= 1
        return self.grid

    def expand_right(self):
        self.grid = [l + ["."] for l in self.grid]
        self.grid[-1][-1] = "#"
        return self.grid

    def drop_sand(self, start_x=500):
        grid = self.grid
        x = start_x - self.x_min
        y = 0
        if self.grid[y][x] != ".":
            return False

        while True:
            # check fall through
            if y + 1 == len(grid):
                return False

            # try to move down
            if grid[y + 1][x] == ".":
                y += 1
                continue

            if x == 0:
                grid = self.expand_left()
                x = 1
            elif x + 1 == len(grid[0]):
                grid = self.expand_right()

            # try to move down left
            if grid[y + 1][x - 1] == ".":
                y += 1
                x -= 1
                continue

            # try to move down right
            if grid[y + 1][x + 1] == ".":
                y += 1
                x += 1
                continue

            # cannot move
            break

        grid[y][x] = "o"
        self.n_sand += 1
        return True


p2 = P2(inp)
while p2.drop_sand():
    ...

# p2.print_grid()
print("Part 2:", p2.n_sand)
