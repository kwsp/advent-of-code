import re

with open("day1.txt", "r") as fp:
    s = fp.read().strip()
    lines = s.split("\n")

part1 = 0
for l in lines:
    d = re.findall(r"\d", l)
    part1 += int(d[0]) * 10 + int(d[-1])
print(f"{part1=}")


numstr = r"one|two|three|four|five|six|seven|eight|nine"
lookup: dict[str, int] = {}
for i, s in enumerate(numstr.split("|"), 1):
    lookup[str(i)] = i
    lookup[s] = i
    lookup[s[::-1]] = i

pat_forward = re.compile("(" f"{numstr}" r"|\d)")
pat_backward = re.compile("(" f"{numstr[::-1]}" r"|\d)")

part2 = 0
nums = []
for l in lines:
    a = lookup[next(pat_forward.finditer(l)).group()]
    b = lookup[next(pat_backward.finditer(l[::-1])).group()]
    nums.append(a * 10 + b)
part2 = sum(nums)
print(f"{part2=}")
