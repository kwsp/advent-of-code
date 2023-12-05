import enum


class Move(enum.IntEnum):
    rock = 1
    paper = 2
    scissors = 3


m1 = {"A": Move.rock, "B": Move.paper, "C": Move.scissors}
m2 = {"X": Move.rock, "Y": Move.paper, "Z": Move.scissors}


class Outcome(enum.IntEnum):
    loss = 0
    draw = 3
    win = 6


def check_outcome(op_move: Move, your_move: Move) -> Outcome:
    if op_move == your_move:
        return Outcome.draw

    if op_move == Move.rock:
        if your_move == Move.paper:
            return Outcome.win
    elif op_move == Move.paper:
        if your_move == Move.scissors:
            return Outcome.win
    else:  # op_move == Move.scissors
        if your_move == Move.rock:
            return Outcome.win
    return Outcome.loss


def get_move(op_move: Move, outcome: Outcome) -> Move:
    if outcome == outcome.draw:
        return op_move

    if outcome == outcome.win:
        if op_move == Move.scissors:
            return Move.rock
        elif op_move == Move.rock:
            return Move.paper
        # op_move == Move.paper
        return Move.scissors

    # elif outcome == outcome.loss:
    if op_move == Move.scissors:
        return Move.paper
    elif op_move == Move.rock:
        return Move.scissors
    # op_move == Move.paper
    return Move.rock


with open("./day02.txt") as fp:
    lines = fp.read().strip().split("\n")

strat = [line.split(" ") for line in lines]

total_score = 0
for op_move, your_move in strat:
    op_move = m1[op_move]
    your_move = m2[your_move]
    outcome = check_outcome(op_move, your_move)
    total_score += your_move + outcome

print("Part 1:", total_score)


m3 = {"X": Outcome.loss, "Y": Outcome.draw, "Z": Outcome.win}

total_score = 0
for op_move, outcome in strat:
    op_move = m1[op_move]
    outcome = m3[outcome]
    your_move = get_move(op_move, outcome)
    total_score += your_move + outcome

print("Part 2:", total_score)
