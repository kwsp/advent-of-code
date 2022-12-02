from collections import defaultdict
from functools import lru_cache


def load_input(path):
    with open(path) as f:
        data = f.read().strip().split()
    return sorted([int(d) for d in data])


def find_path(data, start=0, diff=3):
    if data[-1] - start <= diff:
        return [data[-1]]
    for i, d in enumerate(data):
        if d - start > diff:
            break
        res = find_path(data[i + 1 :], d, diff)
        if res is not None:
            return [d, *res]
    return None


def find_all_path(data, curr=0, diff=3):
    @lru_cache(maxsize=1000)
    def find_all_path_worker(start=curr, curr=curr, diff=diff):
        if data[-1] - curr <= diff:
            return 1

        n = 0
        for i in range(start, len(data)):
            if data[i] - curr > diff:
                break
            res = find_all_path_worker(i + 1, data[i], diff)
            n += res
        return n

    return find_all_path_worker(0, curr, diff)


if __name__ == "__main__":
    path = "./day10input.txt"
    data = load_input(path)

    res = find_path(data)

    d: dict = defaultdict(lambda: 0)
    prev = 0
    for i, v in enumerate(data):
        diff = v - prev
        prev = v
        d[diff] += 1

    d[3] += 1  # built-int adaptor always 3+

    print("Part 1:", d[1] * d[3])

    data.append(data[-1] + 3)
    res = find_all_path(data)
    print("Part 2:", res)
