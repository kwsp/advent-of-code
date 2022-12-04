from __future__ import annotations
from dataclasses import dataclass
import math
import copy

import graphviz


@dataclass
class Leaf:
    val: int
    parent: Node | None = None
    name: str | None = None

    def __repr__(self):
        return f"{self.val}"

    def __add__(self, v):
        self.val += v
        return self

    def magnitude(self) -> int:
        return self.val


@dataclass
class Node:
    left: Node | Leaf
    right: Node | Leaf
    parent: Node | None = None
    name: str | None = None

    def __init__(self, left: Node | Leaf | int, right: Node | Leaf | int, parent=None):
        self.left = Leaf(left) if isinstance(left, int) else left
        self.right = Leaf(right) if isinstance(right, int) else right

        self.left.parent = self
        self.right.parent = self
        if parent:
            self.parent = parent

    def __repr__(self):
        return f"Node({self.left}, {self.right})"

    def __add__(self, other: Node):
        return Node(copy.deepcopy(self), copy.deepcopy(other))

    def dot(self, fname=None, highlight: list[int] = []) -> str:
        stack: list[Node | Leaf] = [self]

        node_i = 0
        leaf_i = 0
        orders_visited: list[Node | Leaf] = []

        _dot = graphviz.Digraph("G")

        while stack:
            curr = stack.pop()

            if isinstance(curr, Node):
                stack.append(curr.right)
                stack.append(curr.left)

                orders_visited.append(curr)
                name = f"n{node_i}"
                curr.name = name
                node_i += 1

                _dot.node(name)
            else:
                name = f"l{leaf_i}"
                curr.name = name
                orders_visited.append(curr)
                leaf_i += 1

                if id(curr) in highlight:
                    _dot.node(
                        name,
                        str(curr.val),
                        shape="doublecircle",
                        style="filled",
                        color="yellow",
                    )
                else:
                    _dot.node(name, str(curr.val), shape="doublecircle", style="filled")

        for node in orders_visited:
            name = node.name
            assert name is not None
            if isinstance(node, Node):
                l = node.left
                r = node.right
                ln = l.name
                rn = r.name
                assert ln is not None
                assert rn is not None

                _dot.edge(name, ln)
                _dot.edge(name, rn)

        if isinstance(fname, str):
            with open(fname, "w") as fp:
                fp.write(_dot.source)

        return _dot.source

    @staticmethod
    def from_list(inp: list) -> Node:
        assert len(inp) == 2
        left = inp[0]
        right = inp[1]
        if isinstance(left, list):
            left = Node.from_list(left)

        if isinstance(right, list):
            right = Node.from_list(right)

        this = Node(left, right)
        return this

    @staticmethod
    def from_str(inp: str) -> Node:
        return Node.from_list(eval(inp))

    def to_list(self) -> list:
        left = self.left
        right = self.right
        if isinstance(left, Node):
            left = left.to_list()
        else:
            left = left.val
        if isinstance(right, Node):
            right = right.to_list()
        else:
            right = right.val
        return [left, right]

    @property
    def l(self):
        return self.to_list()

    def explode(self):
        explode(self)

    def split(self):
        split(self)

    def magnitude(self):
        return self.left.magnitude() * 3 + self.right.magnitude() * 2


def add_to_next_leaf(stack: list[tuple[Node | Leaf, int]], val: int):
    while stack:
        curr, _ = stack.pop()
        if isinstance(curr, Node):
            stack.append((curr.right, -1))
            stack.append((curr.left, -1))
        else:
            curr.val += val
            return


def explode(inp: Node, viz: list[str] | None = None) -> bool:
    "Inplace"
    stack: list[tuple[Node | Leaf, int]] = [(inp, 1)]
    last_leaf = None
    while stack:
        curr, depth = stack.pop()
        if isinstance(curr, Node):

            ### Explode
            if depth > 4:
                assert isinstance(curr.left, Leaf)
                assert isinstance(curr.right, Leaf)

                # If viz, make graphviz before and after
                if viz is not None:
                    s = inp.dot(highlight=[id(curr.left), id(curr.right)])
                    viz.append(s)

                if last_leaf:
                    last_leaf.val += curr.left.val

                add_to_next_leaf(stack, curr.right.val)

                parent = curr.parent
                if parent is not None:
                    new_leaf = Leaf(0, parent)
                    if parent.left is curr:
                        parent.left = new_leaf
                    else:
                        parent.right = new_leaf
                return True

            stack.append((curr.right, depth + 1))
            stack.append((curr.left, depth + 1))

        else:  # isinstance(curr, Leaf)
            # print(curr.val)
            last_leaf = curr

    return False


def split(inp: Node, viz: list[str] | None = None) -> bool:
    "Inplace"
    stack: list[Node | Leaf] = [inp]
    while stack:
        curr = stack.pop()
        if isinstance(curr, Node):
            stack.append(curr.right)
            stack.append(curr.left)
        else:
            if curr.val >= 10:
                parent = curr.parent
                assert isinstance(parent, Node)

                if viz is not None:
                    s = inp.dot(highlight=[id(curr)])
                    viz.append(s)

                tmp = curr.val / 2
                new_node = Node(math.floor(tmp), math.ceil(tmp), parent=parent)
                if parent.left == curr:
                    parent.left = new_node
                if parent.right == curr:
                    parent.right = new_node
                return True
    return False


# test explode
def test_explode(before: str, after: str):
    n = Node.from_str(before)
    explode(n)
    assert n.l == eval(after)

    n = Node.from_str(before)
    explode(n, [])
    assert n.l == eval(after)


test_explode("[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]")
test_explode("[7,[6,[5,[4,[3,2]]]]]", "[7,[6,[5,[7,0]]]]")
test_explode("[[6,[5,[4,[3,2]]]],1]", "[[6,[5,[7,0]]],3]")
test_explode(
    "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"
)
test_explode("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[7,0]]]]")

test_explode(
    "[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]", "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"
)

# test split
def test_split(before: str, after: str):
    n = Node.from_str(before)
    split(n)
    assert n.l == eval(after)

    n = Node.from_str(before)
    split(n, [])
    assert n.l == eval(after)


test_split("[[[[0,7],4],[15,[0,13]]],[1,1]]", "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]")
test_split(
    "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]", "[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]"
)


def reduce(inp: Node, viz: list | None = []):
    while True:
        # print(inp.l)
        if explode(inp, viz=viz):
            # print("Explode: ", end="")
            continue
        if split(inp, viz=viz):
            # print("Split:   ", end="")
            continue
        break

    # print()

    if viz is not None:
        viz.append(inp.dot())

    return inp


# test_reduce


def test_reduce(inp_: str, expect_: str):
    inp = Node.from_str(inp_)
    expect = Node.from_str(expect_)
    reduced = reduce(inp, [])
    assert reduced.l == expect.l


test_reduce("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[7,0]]]]")
test_reduce(
    "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]", "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"
)


def dfs(inp: Node):
    stack: list[Node | Leaf] = [inp]
    while stack:
        curr = stack.pop()
        if isinstance(curr, Node):
            stack.append(curr.right)
            stack.append(curr.left)
        else:
            print(curr.val)


# test addition
def test_addition(a: str, b: str, after: str):
    n1 = Node.from_str(a)
    n2 = Node.from_str(b)
    n3 = reduce(n1 + n2, [])

    this = n3.l
    truth = eval(after)

    if this != truth:
        from pprint import pprint

        print("Addition wrong")
        print("Expected:")
        pprint(truth)
        print("Got:")
        pprint(this)


test_addition(
    "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]",
    "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]",
    "[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]",
)


def write_viz(viz: list[str], dirname="viz"):
    from pathlib import Path
    from tqdm import tqdm

    d = Path(dirname)
    d.mkdir()
    for i, s in tqdm(enumerate(viz), total=len(viz)):
        fname = str(d / f"{i:02d}.dot")
        # write DOT
        with open(fname, "w") as fp:
            fp.write(s)

        # write SVG
        svg_fname = str(d / f"{i:02d}.svg")
        graphviz.render("dot", "svg", fname, outfile=svg_fname)


test_addition(
    "[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]",
    "[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]",
    "[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]",
)

test_addition(
    "[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]",
    "[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]",
    "[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]",
)

# n1 = Node.from_str("[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]")
# n2 = Node.from_str("[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]")
# viz = []
# n3 = reduce(n1 + n2, viz)
# write_viz(viz)


test_addition(
    "[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]",
    "[7,[5,[[3,8],[1,4]]]]",
    "[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]",
)


def sum_nodes(l: list[Node]) -> Node:
    res = l[0]
    for n in l[1:]:
        # print(f"Adding {res.l} to {n.l}")
        res += n
        reduce(res, [])
    return res


def sum_nodes_str(l: str) -> Node:
    ns = [Node.from_list(eval(i)) for i in l.strip().split("\n")]
    return sum_nodes(ns)


# test sum result
assert (
    sum_nodes_str(
        """
[1,1]
[2,2]
[3,3]
[4,4]
"""
    ).l
    == eval("[[[[1,1],[2,2]],[3,3]],[4,4]]")
)

assert (
    sum_nodes_str(
        """
[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
"""
    ).l
    == eval("[[[[3,0],[5,3]],[4,4]],[5,5]]")
)

assert (
    sum_nodes_str(
        """
[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]
"""
    ).l
    == eval("[[[[5,0],[7,4]],[5,5]],[6,6]]")
)

assert (
    sum_nodes_str(
        """
[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]
"""
    ).l
    == eval("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]")
)


# test magnitude
assert Node.from_str("[[1,2],[[3,4],5]]").magnitude() == 143
assert Node.from_str("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]").magnitude() == 1384
assert Node.from_str("[[[[1,1],[2,2]],[3,3]],[4,4]]").magnitude() == 445
assert Node.from_str("[[[[3,0],[5,3]],[4,4]],[5,5]]").magnitude() == 791
assert Node.from_str("[[[[5,0],[7,4]],[5,5]],[6,6]]").magnitude() == 1137
assert (
    Node.from_str("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]").magnitude()
    == 3488
)

s = sum_nodes_str(
    """
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
"""
)
assert s.l == [
    [[[6, 6], [7, 6]], [[7, 7], [7, 0]]],
    [[[7, 7], [7, 7]], [[7, 8], [9, 9]]],
]

assert s.magnitude() == 4140

## Part 1
with open("./day18.txt", "r") as fp:
    inp = fp.read()

res = sum_nodes_str(inp)
print("Part 1:", res.magnitude())

## Part 2
from itertools import combinations
from tqdm import tqdm

l = inp
nodes = [Node.from_list(eval(i)) for i in l.strip().split("\n")]

_max = 0
for a, b in tqdm(list(combinations(nodes, 2))):
    v = reduce(a + b, []).magnitude()
    _max = max(_max, v)
    v = reduce(a + b, []).magnitude()
    _max = max(_max, v)

print("Part 2:", _max)
