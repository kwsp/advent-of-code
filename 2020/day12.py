def read_input(path):
    with open(path) as f:
        raw = f.read()
    return raw.strip().split("\n")


def execute(instructions, x=0, y=0, degree=90):
    for ins in instructions:
        if ins[0] == "N":
            y += int(ins[1:])
        elif ins[0] == "S":
            y -= int(ins[1:])
        elif ins[0] == "W":
            x -= int(ins[1:])
        elif ins[0] == "E":
            x += int(ins[1:])
        elif ins[0] == "R":
            degree += int(ins[1:])
            degree %= 360
        elif ins[0] == "L":
            degree -= int(ins[1:])
            degree %= 360
        elif ins[0] == "F":
            if degree == 0:
                y += int(ins[1:])
            elif degree == 180:
                y -= int(ins[1:])
            elif degree == 270:
                x -= int(ins[1:])
            elif degree == 90:
                x += int(ins[1:])
            else:
                raise ValueError("degree unknown: ", degree)
        else:
            raise ValueError("Unknown instruction: ", ins)

    return x, y, degree


def execute2(instructions, x=0, y=0):
    way_x, way_y = 10, 1
    for ins in instructions:
        if ins[0] == "N":
            way_y += int(ins[1:])
        elif ins[0] == "S":
            way_y -= int(ins[1:])
        elif ins[0] == "W":
            way_x -= int(ins[1:])
        elif ins[0] == "E":
            way_x += int(ins[1:])

        elif ins[0] == "R":
            degree = int(ins[1:])
            degree %= 360
            if degree == 90:
                way_x, way_y = way_y, -way_x
            elif degree == 180:
                way_x, way_y = -way_x, -way_y
            elif degree == 270:
                way_x, way_y = -way_y, way_x
            else:
                raise ValueError("degree unknown: ", degree)

        elif ins[0] == "L":
            degree = int(ins[1:])
            degree %= 360
            if degree == 90:
                way_x, way_y = -way_y, way_x
            elif degree == 180:
                way_x, way_y = -way_x, -way_y
            elif degree == 270:
                way_x, way_y = way_y, -way_x
            else:
                raise ValueError("degree unknown: ", degree)

        elif ins[0] == "F":
            n = int(ins[1:])
            x += way_x * n
            y += way_y * n
        else:
            raise ValueError("Unknown instruction: ", ins)
        #  print(f"ins: {ins}, x: {x}, y: {y}, way_x: {way_x}, way_y: {way_y}")

    return x, y


if __name__ == "__main__":
    data = read_input("./day12input.txt")
    x, y, degree = execute(data)
    print("Part1: ", abs(x) + abs(y))

    x, y = execute2(data)
    print("Part2: ", abs(x) + abs(y))
