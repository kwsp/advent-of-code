from typing import NamedTuple
from queue import PriorityQueue


with open("./day12.txt") as fp:
    s = fp.read()

lines = s.strip().split("\n")


class Pos(NamedTuple):
    x: int
    y: int


class Part1:
    def __init__(self, lines):
        self.lines = lines
        self.Y = len(lines)
        self.X = len(lines[0])
        self.cost = [[int(1e9) for _ in range(self.X)] for _ in range(self.Y)]

        for j, l in enumerate(lines):
            for i, c in enumerate(l):
                if c == "S":
                    self.start = Pos(i, j)
                elif c == "E":
                    self.end = Pos(i, j)

    def set_cost(self, pos: Pos, c: int):
        self.cost[pos.y][pos.x] = c

    def get_cost(self, pos: Pos) -> int:
        return self.cost[pos.y][pos.x]

    def get_neighbours(self, pos: Pos):
        neighbours = []
        if pos.x > 0:
            neighbours.append(Pos(x=pos.x - 1, y=pos.y))
        if pos.y > 0:
            neighbours.append(Pos(x=pos.x, y=pos.y - 1))
        if pos.x < self.X - 1:
            neighbours.append(Pos(x=pos.x + 1, y=pos.y))
        if pos.y < self.Y - 1:
            neighbours.append(Pos(x=pos.x, y=pos.y + 1))
        return neighbours

    def get_height(self, pos: Pos) -> int:
        c = self.lines[pos.y][pos.x]
        if c == "S":
            return ord("a")
        if c == "E":
            return ord("z")
        return ord(c)

    def find(self):
        q = PriorityQueue()

        q.put((0, self.start))
        while not q.empty():
            cost, pos = q.get()
            if pos == self.end:
                return cost

            # print(f"Visiting {pos} {cost=}")

            height = self.get_height(pos)

            new_cost = cost + 1

            for nei in self.get_neighbours(pos):
                nei_height = self.get_height(nei)
                if nei_height - height <= 1 and new_cost < self.get_cost(nei):
                    self.set_cost(nei, new_cost)
                    q.put((new_cost, nei))


p1 = Part1(lines)
print("Part 1:", p1.find())


class Part2(Part1):
    def find(self):
        q = PriorityQueue()

        q.put((0, self.start))
        while not q.empty():
            cost, pos = q.get()
            if pos == self.end:
                return cost + 1

            height = self.get_height(pos)

            if height != ord("a"):
                new_cost = cost + 1
            else:
                new_cost = cost

            for nei in self.get_neighbours(pos):
                nei_height = self.get_height(nei)
                if nei_height - height <= 1 and new_cost < self.get_cost(nei):
                    self.set_cost(nei, new_cost)
                    q.put((new_cost, nei))


p2 = Part2(lines)
print("Part 2:", p2.find())
