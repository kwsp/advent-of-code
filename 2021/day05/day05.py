def loadInput(fname="day05.txt"):
    with open(fname, "r") as fp:
        lines = fp.read().strip().split("\n")
    inp = []
    _max = 0
    for line in lines:
        curr = []
        for pts in line.split(" -> "):
            a, b = map(int, pts.split(","))
            _max = max(a, max(b, _max))
            curr.append([a, b])
        inp.append(curr)
    return inp, _max + 1


def part2():
    inp, _max = loadInput("day05.txt")
    mat = [[0] * _max for _ in range(_max)]

    for (pt1, pt2) in inp:
        if pt1[0] == pt2[0]:
            s, e = min(pt1[1], pt2[1]), max(pt1[1], pt2[1])
            for i in range(s, e + 1):
                mat[pt1[0]][i] += 1
        elif pt1[1] == pt2[1]:
            s, e = min(pt1[0], pt2[0]), max(pt1[0], pt2[0])
            for i in range(s, e + 1):
                mat[i][pt1[1]] += 1
        elif abs(pt2[1] - pt1[1]) == abs(pt2[0] - pt1[0]):  # diagonal
            s1, e1 = pt1[0], pt2[0]
            step1 = 1 if s1 < e1 else -1
            s2, e2 = pt1[1], pt2[1]
            step2 = 1 if s2 < e2 else -1
            for d1, d2 in zip(
                range(0, e1 - s1 + step1, step1), range(0, e2 - s2 + step2, step2)
            ):
                mat[s1 + d1][s2 + d2] += 1

    cnt = 0
    for line in mat:
        for v in line:
            cnt += v > 1
    print("Part 2:", cnt)


def printmat(mat):
    p = lambda x: str(x) if x > 0 else "."
    for i in range(len(mat[0])):
        s = "".join([p(mat[j][i]) for j in range(len(mat))])
        print(s)


def part1():
    inp, _max = loadInput("day051.txt")
    mat = [[0] * _max for _ in range(_max)]

    for (pt1, pt2) in inp:
        if pt1[0] == pt2[0]:
            s, e = min(pt1[1], pt2[1]), max(pt1[1], pt2[1])
            for i in range(s, e + 1):
                mat[pt1[0]][i] += 1
        elif pt1[1] == pt2[1]:
            s, e = min(pt1[0], pt2[0]), max(pt1[0], pt2[0])
            for i in range(s, e + 1):
                mat[i][pt1[1]] += 1

    cnt = 0
    for line in mat:
        for v in line:
            cnt += v > 1

    print("Part 1:", cnt)


part1()
part2()
