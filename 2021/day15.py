from typing import TypeVar
from queue import SimpleQueue

with open("day151.txt") as fp:
    lines = fp.read().strip().split("\n")

mat = []
for line in lines:
    mat.append([int(i) for i in line])


T = TypeVar("T")
Mat2d = list[list[T]]

def _mat2d(Y: int, X: int, init_val=None) -> Mat2d:
    "Make a 2D mat of size (Y, X) with init_val"
    return [[init_val] * X for _ in range(Y)]


def shortest_path(mat: Mat2d[int], start_coord: tuple[int, int]):
    Y = len(mat)
    X = len(mat[0])
    distance = _mat2d(Y, X, float("inf"))  # shortest distance to (y, x)
    predecessor = _mat2d(Y, X)

    Node = tuple[int, int]  # coordinate (Y, X)

    def get_neighbours(node: Node) -> list[Node]:
        res = []
        up = (node[0] - 1, node[1])
        down = (node[0] + 1, node[1])
        left = (node[0], node[1] - 1)
        right = (node[0], node[1] + 1)
        if up[0] >= 0:
            res.append(up)
        if down[0] < Y:
            res.append(down)
        if left[1] >= 0:
            res.append(left)
        if right[1] < X:
            res.append(right)
        return res

    def getv(mat: Mat2d[int], key: Node):
        return mat[key[0]][key[1]]

    def setv(mat: Mat2d[int], key: Node, val: int):
        mat[key[0]][key[1]] = val

    setv(distance, start_coord, 0)

    q = SimpleQueue()
    q.put(start_coord)
    seen = set()
    while not q.empty():
        node = q.get()
        node_dist = getv(distance, node)
        for neighbour in get_neighbours(node):
            new_dist = node_dist + getv(mat, neighbour)
            if new_dist < getv(distance, neighbour):
                setv(distance, neighbour, new_dist)
                setv(predecessor, neighbour, node)
                q.put(neighbour)
            elif neighbour not in seen:
                q.put(neighbour)

            seen.add(neighbour)

    return distance, predecessor

distance, predecessor = shortest_path(mat, (0, 0))
print("Part 1:", distance[-1][-1])


def increment_list(l: list, _max=9):
    """
    Return a copy of l with every element incremented by 1
    and wraps around max value of _max
    """
    return [(v % _max) + 1 for v in l]
    

def tile_mat(mat: Mat2d, N=5) -> Mat2d:
    htiled = []
    for row in mat:
        # every row
        curr_row = []

        row_inc = [v for v in row]
        curr_row.extend(row_inc)

        for _ in range(N - 1):
            row_inc = increment_list(row_inc)
            curr_row.extend(row_inc)

        htiled.append(curr_row)


    vtiled = []
    htiled_inc = [row for row in htiled]
    vtiled.extend(htiled_inc)
    for _ in range(N - 1):
        htiled_inc = [increment_list(row) for row in htiled_inc]
        vtiled.extend(htiled_inc)
    return vtiled

tiled = tile_mat(mat)
distance, predecessor = shortest_path(tiled, (0, 0))
print("Part 2:", distance[-1][-1])
