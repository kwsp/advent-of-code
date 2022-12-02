with open("./day01.txt") as fp:
    elfs = fp.read().strip().split("\n\n")


elfs = [[int(x) for x in elf.split("\n")] for elf in elfs]
sums = [sum(elf) for elf in elfs]

part1 = max(sums)
print("Part 1:", part1)


sums.sort()
sums[-3:]

part2 = sum(sums[-3:])

print("Part 2:", part2)
