with open("./inp.txt", "r") as fp:
    inp = [
        [[int(i) for i in p.strip().split()] for p in l.split("|", 1)]
        for l in (l.rstrip("\n").split(":")[1] for l in fp)
    ]
    N = len(inp)

won = [sum(1 for i in b if i in a) for a, b in inp]
part1 = sum(2 ** (n - 1) for n in won if n > 0)
print(f"{part1=}")

own = [1] * N
for i, w in enumerate(won):
    for j in range(i + 1, min(i + w + 1, N)):
        own[j] += own[i]

part2 = sum(own)
print(f"{part2=}")
