from operator import mul
from functools import reduce


def traverse(inp, right, down):
    X = len(inp[0])
    Y = len(inp)
    trees = 0
    x, y = 0, 0
    while y < Y:
        trees += inp[y][x % X] == "#"
        x += right
        y += down
    return trees


def solutionPart1(inp):
    return traverse(inp, 3, 1)


def solutionPart2(inp):
    right_down = ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))
    return reduce(mul, [traverse(inp, p[0], p[1]) for p in right_down])


def loadInput(path):
    with open(path) as f:
        data = f.read().strip().split("\n")
    return data


if __name__ == "__main__":
    inp = loadInput("./day03input.txt")
    s = solutionPart1(inp)
    print("Part 1: ", s)
    s = solutionPart2(inp)
    print("Part 2: ", s)
