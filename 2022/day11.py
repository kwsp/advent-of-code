from typing import Callable
from dataclasses import dataclass

s = """
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""

with open("./day11.txt") as fp:
    s = fp.read()


@dataclass
class Monkey:
    items: list[int]
    op: Callable[[int], int]
    test_mod: int
    test_t: int
    test_f: int

    n_inspects: int = 0

    @classmethod
    def parse(cls, s: str):
        lines = s.split("\n")
        assert lines[0].startswith("Monkey")
        items = [int(v) for v in lines[1].split(":")[-1].split(",")]
        op = eval("lambda old: " + lines[2].split("=")[-1])

        test_mod = int(lines[3].rsplit(maxsplit=1)[-1].strip())
        test_t = int(lines[4].rsplit(maxsplit=1)[-1].strip())
        test_f = int(lines[5].rsplit(maxsplit=1)[-1].strip())

        return cls(items, op, test_mod, test_t, test_f)

    def manage_worry(self, item: int):
        "Part 1"
        return item // 3

    def throw(self):
        for item in self.items:
            self.n_inspects += 1

            item = self.op(item)
            item = self.manage_worry(item)

            if item % self.test_mod == 0:
                yield self.test_t, item
            else:
                yield self.test_f, item

    def catch(self, item: int):
        self.items.append(item)


def print_(monkeys: list[Monkey]):
    for i, monkey in enumerate(monkeys):
        print(f"Monkey {i}: {monkey.items}")


def do_round(monkeys: list[Monkey]):
    for monkey in monkeys:
        for i, item in monkey.throw():
            monkeys[i].catch(item)
        monkey.items = []


def part1():
    monkeys: list[Monkey] = [Monkey.parse(ss) for ss in s.strip().split("\n\n")]
    for _ in range(20):
        do_round(monkeys)
    ns = [m.n_inspects for m in monkeys]
    ns.sort()
    print("Part 1:", ns[-1] * ns[-2])


part1()


class Monkey2(Monkey):
    _mod = 0

    def manage_worry(self, item: int):
        return item % self._mod


def part2():
    monkeys: list[Monkey] = [Monkey2.parse(ss) for ss in s.strip().split("\n\n")]

    from functools import reduce
    from operator import mul

    Monkey2._mod = reduce(mul, [m.test_mod for m in monkeys])

    for _ in range(10000):
        do_round(monkeys)

    ns = [m.n_inspects for m in monkeys]
    ns.sort()
    print("Part 2:", ns[-1] * ns[-2])


part2()
