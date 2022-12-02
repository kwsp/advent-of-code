def parse_board(board):
    rows = []
    board.split("\n")
    rows = [[int(i) for i in row.split()] for row in board.split("\n")]
    cols = [[row[i] for row in rows] for i in range(len(rows))]
    return (rows, cols)


def get_input(fname="day04.txt"):
    with open(fname, "r") as fp:
        raw = fp.read().strip().split("\n\n")
        q = [int(i) for i in raw[0].split(",")]
        boards = [parse_board(b) for b in raw[1:]]
    return q, boards


def check_winners(boards, seen):
    winners = set()
    for i, board in enumerate(boards):
        for line in [*board[0], *board[1]]:
            if not [l for l in line if l not in seen]:
                winners.add(i)
    return winners


def check_winner(boards, seen):
    for i, board in enumerate(boards):
        for line in [*board[0], *board[1]]:
            if not [l for l in line if l not in seen]:
                return i
    return None


def part2():
    q, boards = get_input()
    seen = set()
    for x in q:
        seen.add(x)
        winners = check_winners(boards, seen)
        w_boards = [b for i, b in enumerate(boards) if i in winners]
        boards = [b for i, b in enumerate(boards) if not i in winners]
        if len(boards) == 0:
            acc = 0
            for line in w_boards[0][0]:
                for v in line:
                    if not v in seen:
                        acc += v
            print("Part 2:", acc * x)
            return


def part1():
    q, boards = get_input()
    seen = set()
    for x in q:
        seen.add(x)
        winner = check_winners(boards, seen)
        if winner:
            acc = 0
            for line in boards[winner.pop()][0]:
                for v in line:
                    if not v in seen:
                        acc += v
            print("Part 1:", acc * x)
            return


part1()
part2()
