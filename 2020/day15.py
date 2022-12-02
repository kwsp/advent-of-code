from collections import defaultdict
with open("day15.txt") as fp:
    raw = fp.read().strip().split(",")
    data = [int(i) for i in raw]

when = defaultdict(list)
for i, k in enumerate(data):
    when[k].append(i+1)

i = len(data) + 1
last_spoke = data[-1]
while i <= 30000000:
    if last_spoke in when:
        if len(when[last_spoke]) < 2:
            last_spoke = 0
        else:
            last_spoke = when[last_spoke][-1] - when[last_spoke][-2]

        when[last_spoke].append(i)
        if len(when[last_spoke]) > 2:
            when[last_spoke] = when[last_spoke][-2:]
    else:
        when[0] = [i]
        last_spoke = 0
    i += 1

print(last_spoke)
