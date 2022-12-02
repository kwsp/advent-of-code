def loadInput(path):
    with open(path) as f:
        raw = f.read().strip().split("\n")

    data = [r.split(": ") for r in raw]
    return data


def solutionPart1(data):
    nvalid = 0
    for rule, pswd in data:
        rpt, char = rule.split(" ")
        i = rpt.find("-")
        low = int(rpt[:i])
        high = int(rpt[i + 1 :])
        c = pswd.count(char)
        if c >= low and c <= high:
            nvalid += 1
    return nvalid


def solutionPart2(data):
    nvalid = 0
    for rule, pswd in data:
        rpt, char = rule.split(" ")
        i = rpt.find("-")
        low = int(rpt[:i])
        high = int(rpt[i + 1 :])
        c = (pswd[low - 1] == char) + (pswd[high - 1] == char)
        if c == 1:
            nvalid += 1
    return nvalid


if __name__ == "__main__":
    data = loadInput("./day02input.txt")

    s = solutionPart1(data)
    print("Part 1: ", s)
    s = solutionPart2(data)
    print("Part 2: ", s)
