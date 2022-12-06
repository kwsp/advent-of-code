with open("day13.txt") as fp:
    raw = fp.read().strip().split("\n")
    s = int(raw[0])
    bs = raw[1].split(",")

bid = [int(i) for i in bs if i != "x"]
nt = min([(s + b - s % b, b) for b in bid], key=lambda x: x[0])
print("Part 1:", (nt[0] - s) * nt[1])


def find(ans, val, offset, incr):
    while True:
        if (ans + offset) % val == 0:
            return ans
        ans += incr


buses = [[int(val), offset] for offset, val in enumerate(bs) if val != "x"]
part2 = buses[0][0]
incr = 1

for bus in buses:
    part2 = find(part2, bus[0], bus[1], incr)
    incr *= bus[0]


print("Part 2:", part2)
