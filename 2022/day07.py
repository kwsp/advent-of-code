from __future__ import annotations
from dataclasses import dataclass

with open("./day07.txt") as fp:
    s = fp.read()

# discard first line "$ cd /"
lines = s.strip().split("\n")[1:]


@dataclass
class File:
    name: str
    parent: Dir | None
    size: int


@dataclass
class Dir:
    name: str
    parent: Dir | None
    ls: dict[str, Dir | File]

    def __hash__(self):
        s = name
        if self.parent:
            s += self.parent.name
        return hash(s)

    @property
    def size(self):
        return sum(i.size for i in self.ls.values())

    def new_entry(self, s: str):
        toks = s.strip().split()
        assert len(toks) == 2
        if toks[0] == "dir":
            name = toks[1]
            self.ls[name] = Dir(name, self, {})
        else:
            size, name = toks
            self.ls[name] = File(name, self, int(size))

    def ls_dir(self) -> list[Dir]:
        return [d for d in self.ls.values() if isinstance(d, Dir)]


N = len(lines)
i = 0

root = cwd = Dir("/", None, {})
while i < N:
    line = lines[i]
    toks = line.split()
    if toks[0] == "$":
        if toks[1] == "cd":
            name = toks[2]
            if name == "..":
                assert cwd.parent is not None
                cwd = cwd.parent
            else:
                try:
                    cwd = cwd.ls[name]
                except Exception as e:
                    breakpoint()
                assert isinstance(cwd, Dir)
            i += 1

        elif toks[1] == "ls":
            j = i + 1
            while j < N and not lines[j].startswith("$"):
                j += 1
            [cwd.new_entry(l) for l in lines[i + 1 : j]]
            i = j

        else:
            breakpoint()
            raise ValueError()


def part1(d: Dir):
    total_size = 0
    seen = set()

    def walk_dir(d: Dir):
        nonlocal total_size, seen
        if d in seen:
            return
        seen.add(d)

        s = d.size
        if s <= 100000:
            total_size += s
        ds = d.ls_dir()
        [walk_dir(d) for d in ds]

    walk_dir(d)
    return total_size


print("Part 1:", part1(root))

TOTAL = 70000000
NEED = 30000000

CURR_FREE = TOTAL - root.size
DEL_SIZE = max(NEED - CURR_FREE, 0)


def part2(d: Dir):
    min_size = d.size
    min_d = d
    seen = set()

    def walk_dir(d: Dir):
        nonlocal min_size, min_d, seen
        if d in seen:
            return
        seen.add(d)

        s = d.size
        if s >= DEL_SIZE:
            if s < min_size:
                min_size = s
                min_d = d

        [walk_dir(dd) for dd in d.ls_dir()]

    walk_dir(d)
    return min_size


print("Part 2:", part2(root))
