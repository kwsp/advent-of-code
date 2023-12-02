with open("./inp.txt", "r") as fp:
    lines = fp.read().strip().split("\n")


Pair = tuple[str, int]
GameSet = list[Pair]
Game = list[GameSet]


def makepair(s: str) -> Pair:
    num, name = s.strip().split()
    return name, int(num)


games: list[Game] = []
for line in lines:
    _, groups = line.split(":", 1)
    game = [[makepair(pair) for pair in g.split(",")] for g in groups.split(";")]
    games.append(game)

part1 = 0
req = dict(
    red=12,
    green=13,
    blue=14,
)
for i, game in enumerate(games, 1):
    if all(v <= req[s] for gs in game for s, v in gs):
        part1 += i
print(f"{part1=}")

from collections import defaultdict
from operator import mul
from functools import reduce

part2 = 0
gamemax: dict[str, int] = defaultdict(int)
for game in games:
    gamemax.clear()
    for name, num in (p for gs in game for p in gs):
        gamemax[name] = max(gamemax[name], num)
    power = reduce(mul, gamemax.values(), 1)
    part2 += power
print(f"{part2=}")
