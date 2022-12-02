from math import sqrt, floor

_inp = "target area: x=20..30, y=-10..-5"

def parse_inp(inp):
    target = tuple(tuple(int(v) for v in s.split("=")[1].split("..")) for s in inp.split(":")[1].split(","))
    return target

# find max number of x steps
def get_x_inf_steps(target):
    return range(floor(sqrt(target[0][0] * 2)), floor(sqrt(target[0][1] * 2)) + 1)

_target = parse_inp(_inp)
_x_steps = get_x_inf_steps(_target)
assert sum(range(_x_steps[0] + 1)) in range(*_target[0])
assert sum(range(_x_steps[1] + 1)) in range(*_target[0])

def get_max_y_height(target):
    init_y = -(min(target[1]) + 1)
    max_y = sum(range(init_y + 1))
    return max_y

assert get_max_y_height(_target) == 45

with open("./day17.txt") as fp:
    inp = fp.read().strip()
target = parse_inp(inp)

max_y = get_max_y_height(target)
print("Part 1:", max_y)


# Part 2
from itertools import product
from collections import defaultdict


def get_possible_x_fly_through(target) -> dict[int, list[int]]:
    "Returns dict(n_step: list(x))"
    x_min = floor(sqrt(min(target[0]) * 2))
    x_max = max(target[0])
    x_target = range(target[0][0], target[0][1] + 1)
    possible_x = defaultdict(list)
    for x in range(x_min, x_max + 1):
        for x_last in range(1, x + 1):
            n_steps = x + 1 - x_last
            pos = sum(range(x_last, x + 1))
            if pos in x_target:
                possible_x[n_steps].append(x)
    return possible_x


def get_possible_y_fly_through(target):
    y_max = -(min(target[1]) + 1)
    y_min = min(target[1])
    possible_y = defaultdict(list)
    y_target = range(target[1][0], target[1][1] + 1)
    for y in range(y_min, y_max + 1):
        for y_last in range(y_min, 0):
            if y_last >= 0:
                continue
            n_steps = y + 1 - y_last
            pos = sum(range(y_last, y + 1))
            if pos in y_target:
                possible_y[n_steps].append(y)
    return possible_y


def get_all_pairs(target):
    possible_x = get_possible_x_fly_through(target)
    possible_y = get_possible_y_fly_through(target)
    
    # cases where y and x both fly through target
    res = []
    for step, _x in possible_x.items():
        if _y := possible_y.get(step):
            res.extend(product(_x, _y))

    # cases where x stops and y keeps dropping
    x_inf_steps = get_x_inf_steps(target)
    max_step_y = max(possible_y.keys())
    for step in x_inf_steps:
        for _step in range(step + 1, max_step_y + 1):
            if _y := possible_y.get(_step):
                res.extend([(step, yy) for yy in _y])

    # res.extend(inf_step_pairs)
    return set(res)

def check_pair(pair, target):
    # check x
    assert sum(range(pair[0] + 1)) in range(*target[0])


assert len(get_all_pairs(_target)) == 112

print("Part 2:", len(get_all_pairs(target)))
