import re
import functools

with open("./day16.txt") as fp:
    _classes, _your, _nearby = fp.read().strip().split("\n\n")


classes = [
    [
        range(int(x), int(y) + 1)
        for x, y in re.findall("(\\d+)-(\\d+)", l.split(":")[1].strip())
    ]
    for l in _classes.split("\n")
]

classes_flat = [r for c in classes for r in c]
parse_ticket = lambda s: [int(i) for i in s.split(",")]
your = parse_ticket(_your.split("\n")[1])
nearby = [parse_ticket(s) for s in _nearby.split("\n")[1:]]


check_ticket_flat = lambda t: [x for x in t if not any(x in r for r in classes_flat)]
p1 = sum([x for n in nearby for x in check_ticket_flat(n)])
print("Part 1:", p1)


valid_tix = [n for n in nearby if not check_ticket_flat(n)]

class2pos = [[] for _ in range(len(classes))]
for class_i, (r1, r2) in enumerate(classes):
    for pos in range(len(classes)):
        l = sum(1 for t in valid_tix if t[pos] in r1 or t[pos] in r2)
        if l == len(valid_tix):
            class2pos[class_i].append(pos)
            continue

# reduce set of class2pos mappings
done = False
while not done:
    # find current len 1 list
    i, val = next(
        (i, l[0])
        for i, l in enumerate(class2pos)
        if isinstance(l, list) and len(l) == 1
    )
    # assign the 1 value to that position
    class2pos[i] = val
    # remove this value from all other lists
    done = not [l.remove(val) for l in class2pos if isinstance(l, list) and val in l]

# class index of "departure ..."
idx = [i for i, l in enumerate(_classes.split("\n")) if l.startswith("departure")]


print(
    "Part 2:",
    functools.reduce(lambda a, b: a * b, [your[class2pos[i]] for i in idx], 1),
)
