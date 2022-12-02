"""
 aaaa    
b    c 
b    c
 dddd 
e    f
e    f
 gggg 

0: abcefg
1: cf
2: acdeg
3: acdfg
4: bcdf
5: abdfg
6: abdefg
7: acf
8: abcdefg
9: abcdfg

2: 1
3: 7
4: 4
5: 2,3,5
6: 0,6,9
7: 8
"""
from collections import Counter

with open("day08.txt") as fp:
    data = []
    for line in fp:
        data.append([pt.strip().split() for pt in line.split("|", 1)])


def get_nmap(ten):
    nmap = {}
    five, six = [], []
    for word in ten:
        if len(word) == 2:
            nmap[1] = set(word)
        elif len(word) == 3:
            nmap[7] = set(word)
        elif len(word) == 4:
            nmap[4] = set(word)
        elif len(word) == 7:
            nmap[8] = set(word)
        elif len(word) == 5:
            five.append(word)
        else:
            six.append(word)

    # 6
    c2 = set([k for k, v in Counter("".join(six)).items() if v == 2])
    c = c2.intersection(nmap[1]).pop()
    w6 = [w for w in six if c not in w][0]
    nmap[6] = set(w6)
    six.remove(w6)

    # 9, 0
    if nmap[4].issubset(six[0]):
        nmap[9] = set(six[0])
        nmap[0] = set(six[1])
    else:
        nmap[9] = set(six[1])
        nmap[0] = set(six[0])

    # 3
    w3 = [w for w in five if nmap[1].issubset(w)][0]
    five.remove(w3)
    nmap[3] = set(w3)

    # 2, 5
    if len(nmap[9].difference(five[0])) == 1:
        nmap[5] = set(five[0])
        nmap[2] = set(five[1])
    else:
        nmap[5] = set(five[1])
        nmap[2] = set(five[0])
    return nmap


def part2():
    s = 0
    for ten, four in data:
        nmap = get_nmap(ten)
        fd = lambda w: [k for k, v in nmap.items() if v == set(w)][0]
        s += int("".join([str(fd(w)) for w in four]))

    print("Part 2:", s)


def part1():
    acc = 0
    for line in data:
        acc += sum([1 for word in line[1] if len(word) in [2, 3, 4, 7]])

    print("Part 1:", acc)


part1()
part2()
