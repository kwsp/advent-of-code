from typing import Tuple, Optional
from functools import reduce

"""
byr (Birth Year)
iyr (Issue Year)
eyr (Expiration Year)
hgt (Height)
hcl (Hair Color)
ecl (Eye Color)
pid (Passport ID)
cid (Country ID)
"""

keys = set(
    (
        "byr",
        "iyr",
        "eyr",
        "hgt",
        "hcl",
        "ecl",
        "pid",
    )
)

ecl_ops = set(("amb", "blu", "brn", "gry", "grn", "hzl", "oth"))


def validateKV(key, val) -> bool:
    if key == "byr":
        v = int(val)
        if v < 1920 or v > 2002:
            return False
    elif key == "iyr":
        v = int(val)
        if v < 2010 or v > 2020:
            return False
    elif key == "eyr":
        v = int(val)
        if v < 2020 or v > 2030:
            return False
    elif key == "hgt":
        if val.endswith("cm"):
            v = int(val[:-2])
            if v < 150 or v > 193:
                return False
        elif val.endswith("in"):
            v = int(val[:-2])
            if v < 59 or v > 76:
                return False
        else:
            return False
    elif key == "hcl":
        if val[0] != "#" or min(val[1:]) < "0" or max(val[1:]) > "f":
            return False
    elif key == "ecl":
        if not val in ecl_ops:
            return False
    elif key == "pid":
        if not (len(val) == 9 and val.isdigit()):
            return False

    return True


def parsePassport(s: str) -> Tuple[bool, dict]:
    d: dict = {}
    nkeys: int = 0
    for vvv in s.split("\n"):
        for vv in vvv.split():
            k, vs = vv.split(":")
            if k in d:
                return False, d
            if k in keys and validateKV(k, vs):
                #  if k in keys:
                d[k] = vs
                nkeys += 1
            elif k == "cid":
                d[k] = vs
            else:
                return False, d
    return nkeys == len(keys), d


def solution(inp):
    parsed = [parsePassport(p) for p in inp]
    return sum(p[0] for p in parsed)


def loadInput(path):
    with open(path) as f:
        data = f.read().split("\n\n")

    return data


if __name__ == "__main__":
    data = loadInput("./day04input.txt")
    s = solution(data)
    print(s)
