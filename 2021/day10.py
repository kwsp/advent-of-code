from functools import reduce

with open("day10.txt") as fp:
    lines = fp.read().split("\n")

open2close = {
    "{": "}",
    "[": "]",
    "(": ")",
    "<": ">",
}
closes = list(open2close.values())

illegal = []
incomplete = []
for line in lines:
    stack = []
    for c in line:
        if c in closes:
            if stack and stack[-1] == c:
                stack.pop()
            else:
                illegal.append(c)
                break
        else:
            stack.append(open2close[c])
    else:
        if stack:
            incomplete.append(stack[::-1])

pts = {")": 3, "]": 57, "}": 1197, ">": 25137}
print("Part 1:", sum([pts[c] for c in illegal]))

incom_pts = {")": 1, "]": 2, "}": 3, ">": 4}
tot = sorted(
    [reduce(lambda acc, c: acc * 5 + incom_pts[c], line, 0) for line in incomplete]
)
print("Part 1:", tot[len(tot) // 2])
