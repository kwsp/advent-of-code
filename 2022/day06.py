def fmarker(s: str, n: int = 4) -> int:
    return next(i + n for i in range(len(s) - n) if len(set(s[i : i + n])) == n)


assert fmarker("bvwbjplbgvbhsrlpgdmjqwftvncz") == 5
assert fmarker("nppdvjthqldpwncqszvftbrmjlhg") == 6
assert fmarker("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 10
assert fmarker("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 11

with open("./day06.txt") as fp:
    inp = fp.read().strip()

print("Part 1:", fmarker(inp))

assert fmarker("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 14) == 19
print("Part 2:", fmarker(inp, 14))
