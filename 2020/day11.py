from copy import deepcopy


def load_input(path):
    with open(path) as f:
        data = f.read().strip().split()
    return [list(d) for d in data]


EMPTY = "L"
OCCUPIED = "#"


def is_occupied(seats, i, j):
    if i >= 0 and j >= 0 and i < len(seats) and j < len(seats[0]):
        return seats[i][j] == OCCUPIED
    return False


def is_empty(seats, i, j):
    #  if i >= 0 and j >= 0 and i < len(seats) and j < len(seats[0]):
    return seats[i][j] == EMPTY
    #  return False


def adjacent_count(seats, i, j):
    "Number of occupied adjacent seats"
    n = 0
    n += is_occupied(seats, i - 1, j - 1)  # up left
    n += is_occupied(seats, i - 1, j)  # up
    n += is_occupied(seats, i - 1, j + 1)  # up right
    n += is_occupied(seats, i, j - 1)  # right
    n += is_occupied(seats, i, j + 1)  # left
    n += is_occupied(seats, i + 1, j - 1)  # up left
    n += is_occupied(seats, i + 1, j)  # down
    n += is_occupied(seats, i + 1, j + 1)  # up right
    return n


def update_seat(old, i, j):
    if is_empty(old, i, j):
        if adjacent_count(old, i, j) == 0:
            return OCCUPIED
    if is_occupied(old, i, j):
        if adjacent_count(old, i, j) >= 4:
            return EMPTY

    return old[i][j]


def update_seats(old):
    new = deepcopy(old)
    for i, row in enumerate(old):
        for j, _ in enumerate(row):
            new[i][j] = update_seat(old, i, j)
    return new


def update_until_stable(old):
    while True:
        new = update_seats(old)
        if new == old:
            return old
        old = new


## Part 2
def is_occupied_edge(seats, i, j, di, dj):
    i = i + di
    j = j + dj
    if i >= 0 and j >= 0 and i < len(seats) and j < len(seats[0]):
        if seats[i][j] == OCCUPIED:
            return True
        elif seats[i][j] == ".":
            return is_occupied_edge(seats, i, j, di, dj)
    return False


def adjacent_count2(seats, i, j):
    "Number of occupied adjacent seats"
    n = 0
    n += is_occupied_edge(seats, i, j, -1, 0)  # up
    n += is_occupied_edge(seats, i, j, -1, -1)  # up left
    n += is_occupied_edge(seats, i, j, -1, +1)  # up right
    n += is_occupied_edge(seats, i, j, 0, -1)  # left
    n += is_occupied_edge(seats, i, j, 0, 1)  # right
    n += is_occupied_edge(seats, i, j, 1, 0)  # down
    n += is_occupied_edge(seats, i, j, 1, -1)  # up left
    n += is_occupied_edge(seats, i, j, 1, +1)  # up right
    return n


def update_seat2(old, i, j):
    if is_empty(old, i, j):
        if adjacent_count2(old, i, j) == 0:
            return OCCUPIED
    if is_occupied(old, i, j):
        if adjacent_count2(old, i, j) >= 5:
            return EMPTY

    return old[i][j]


def update_seats2(old):
    new = deepcopy(old)
    for i, row in enumerate(old):
        for j, _ in enumerate(row):
            new[i][j] = update_seat2(old, i, j)
    return new


def update_until_stable2(old):
    while True:
        new = update_seats2(old)
        if new == old:
            return old
        old = new


## Utils
def print_seats(seats):
    for row in seats:
        print("".join(row))


if __name__ == "__main__":
    data = load_input("day11.txt")

    stable = update_until_stable(data)
    n_occ = sum([l.count(OCCUPIED) for l in stable])
    print("Part 1:", n_occ)

    stable = update_until_stable2(data)
    n_occ = sum([l.count(OCCUPIED) for l in stable])
    print("Part 2:", n_occ)
