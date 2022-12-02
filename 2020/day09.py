from day01 import twoSum


def load_input(path):
    with open(path) as f:
        data = f.read().strip().split()
    return [int(d) for d in data]


def first_non_sum(data: list, preamble: int) -> int:
    for i in range(preamble, len(data)):
        if twoSum(data[i - preamble : i], data[i]) is None:
            return data[i]
    return -1


def contiguous_sum(data: list, sum: int) -> list:
    for i, v in enumerate(data):
        curr = v
        for j, vv in enumerate(data[i + 1 :]):
            curr += vv
            if curr > sum:
                break
            elif curr == sum:
                return data[i : i + j + 2]

    return []


if __name__ == "__main__":
    path = "./day09input.txt"
    data = load_input(path)
    res = first_non_sum(data, 25)
    print("Part 1: ", res)

    res2 = contiguous_sum(data, res)
    res2.sort()
    print("Part 2: ", res2[0] + res2[-1])

    breakpoint()
