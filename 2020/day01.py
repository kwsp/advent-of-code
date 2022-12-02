def twoSum(arr, sum):
    d = {}
    for a in arr:
        if a in d:
            return a, d[a]
        d[sum - a] = a
    return None


def threeSum(arr, sum):
    arr.sort()
    for a in arr:
        res = twoSum(arr, sum - a)
        if res:
            return (a, *res)
    return None


def solutionPart1(arr, sum=2020):
    a, b = twoSum(arr, sum)
    return a * b


def solutionPart2(arr, sum=2020):
    a, b, c = threeSum(arr, sum)
    return a * b * c


def loadInput(path):
    with open(path) as f:
        raw = f.read()
    return [int(d) for d in raw.strip().split()]


if __name__ == "__main__":
    path = "./day01input.txt"

    data = loadInput(path)
    s = solutionPart1(data)
    print("Part 1: ", s)

    data = loadInput(path)
    s = solutionPart2(data)
    print("Part 2: ", s)
