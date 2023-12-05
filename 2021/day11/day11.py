import copy

with open("day111.txt") as fp:
    raw = fp.read().strip().split("\n")
    inp = [[int(i) for i in line] for line in raw]


def increment(data, i, j):
    if i < 0 or j < 0 or i >= len(data) or j >= len(data[0]):
        return
    data[i][j] += 1
    if data[i][j] == 10:
        increment_surround(data, i, j)


def increment_surround(data, i, j):
    increment(data, i, j - 1)
    increment(data, i, j)
    increment(data, i, j + 1)
    increment(data, i - 1, j - 1)
    increment(data, i - 1, j)
    increment(data, i - 1, j + 1)
    increment(data, i + 1, j - 1)
    increment(data, i + 1, j)
    increment(data, i + 1, j + 1)


# part 1
def step(data):
    flashes = 0
    # increase by 1
    for i, line in enumerate(data):
        for j, _ in enumerate(line):
            increment(data, i, j)

    # check flash
    for i, line in enumerate(data):
        for j, _ in enumerate(line):
            if data[i][j] > 9:
                flashes += 1
                data[i][j] = 0
    return flashes


def pprint(data):
    for line in data:
        print("".join([str(i) for i in line]))


def part1():
    data = copy.deepcopy(inp)
    tot = 0
    for _ in range(100):
        f = step(data)
        tot += f
    print("Part 1:", tot)


def part2():
    data = copy.deepcopy(inp)
    tot = 0
    want = len(data[0]) * len(data)
    for i in range(1000000):
        f = step(data)
        if f == want:
            print("Part 2:", i + 1)
            return
        tot += f


part1()
part2()
