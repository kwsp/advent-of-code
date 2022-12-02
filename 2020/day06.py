from collections import Counter


def loadInput(path):
    with open(path) as f:
        raw = f.read()
    return raw.strip().split("\n\n")


def solutionPart1(data):
    total = 0

    for group in data:
        c = Counter()
        c.update(group)
        "\n" in c and c.pop("\n")
        total += len(c)
    return total


def solutionPart2(data):
    total = 0

    for group in data:
        people = group.split("\n")
        s = set(people[0])
        for person in people[1:]:
            s.intersection_update(set(person))
        total += len(s)
    return total


if __name__ == "__main__":
    path = "./day06input.txt"

    data = loadInput(path)
    res = solutionPart1(data)
    print("Part 1: ", res)
    res = solutionPart2(data)
    print("Part 2: ", res)
    breakpoint()
