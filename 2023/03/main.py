with open("./inp.txt", "r") as fp:
    lines = [line.rstrip("\n") for line in fp]

Pos = tuple[int, int]  # row, col
Len = int
Word = tuple[Pos, Len]


def word_len(lines: list[str], pos: Pos) -> Len:
    row, col = pos
    assert lines[row][col].isdigit(), "pos is not on a number"
    if col > 0:
        assert not lines[row][col - 1].isdigit(), "pos not at start of number"
    for j in range(col, len(lines[row])):
        if not lines[row][j].isdigit():
            return j - col
    return len(lines[row]) - col


assert word_len([".123."], (0, 1)) == 3
assert word_len(["$123$"], (0, 1)) == 3
assert word_len([".123"], (0, 1)) == 3
assert word_len(["123."], (0, 0)) == 3
assert word_len(["123$"], (0, 0)) == 3
assert word_len(["...123$"], (0, 3)) == 3


def next_number(lines: list[str], pos: Pos = (0, 0)) -> Word:
    """
    Given a position find the next number.
    If pos is the start of a number, return pos.
    If pos is '.', return start of next number.
    """
    row, col = pos
    # Move past '.' to next number
    i = col
    for j in range(row, len(lines)):
        while i < len(lines[j]):
            if lines[j][i].isdigit():
                pos = (j, i)
                return pos, word_len(lines, pos)
            i += 1
        i = 0
    return (-1, -1), -1


def get_num(lines: list[str], num: Word) -> int:
    (row, col), l = num
    return int(lines[row][col : col + l])


def is_symbol(lines, row, col):
    c = lines[row][col]
    return c != "." and not c.isdigit()


def get_adjacent_symbols(lines, num: Word):
    (row, col), l = num

    symbols: list[Pos] = []

    # check row above
    if row > 0:
        j = row - 1
        for i in range(max(0, col - 1), min(col + l + 1, len(lines[j]))):
            if is_symbol(lines, j, i):
                symbols.append((j, i))

    # check left and right
    if col > 0:
        if is_symbol(lines, row, col - 1):
            symbols.append((row, col - 1))
    if (col + l) < len(lines[row]):
        if is_symbol(lines, row, col + l):
            symbols.append((row, col + l))

    # check row below
    if row < len(lines) - 1:
        j = row + 1
        for i in range(max(0, col - 1), min(col + l + 1, len(lines[j]))):
            if is_symbol(lines, j, i):
                symbols.append((j, i))

    return symbols


assert not get_adjacent_symbols([".123."], ((0, 1), 3))
assert get_adjacent_symbols([".123#"], ((0, 1), 3))
assert get_adjacent_symbols(["#123."], ((0, 1), 3))

part1 = 0

from collections import defaultdict

gears: dict[Pos, list[int]] = defaultdict(list)

num = next_number(lines)
while num[0] != (-1, -1):
    symbols = get_adjacent_symbols(lines, num)
    if symbols:
        v = get_num(lines, num)
        part1 += v

        for symbol_pos in symbols:
            c = lines[symbol_pos[0]][symbol_pos[1]]
            if c == "*":
                gears[symbol_pos].append(v)

    pos, l = num
    num = next_number(lines, (pos[0], pos[1] + l))

print(f"{part1=}")

part2 = 0
for nums in gears.values():
    if len(nums) == 2:
        part2 += nums[0] * nums[1]
print(f"{part2=}")
