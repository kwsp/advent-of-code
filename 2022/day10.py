with open("day10.txt") as fp:
    s = fp.read()


class CPU:
    def __init__(self):
        self.x = 1
        self.clock = 0
        self.pipeline = []
        self.signal_sum = 0
        self.screen: list[str] = [""]

    def check_signal(self):
        if (self.clock - 20) % 40 == 0:
            self.signal_sum += self.clock * self.x

    def draw(self):
        cursor_pos = len(self.screen[-1])
        if cursor_pos >= 40:
            self.screen.append("")
            cursor_pos = 0

        sprite_range = range(self.x - 1, self.x + 2)
        if cursor_pos in sprite_range:
            self.screen[-1] += "#"
        else:
            self.screen[-1] += "."

    def exec(self, op: str):
        if op.startswith("noop"):
            self.clock += 1
            self.check_signal()
            self.draw()
        elif op.startswith("addx"):
            for _ in range(2):
                self.clock += 1
                self.check_signal()
                self.draw()
            self.x += int(op.split(" ")[1])

    def exec_all(self, ops: list[str]):
        for op in ops:
            self.exec(op)


lines = s.strip().split("\n")

cpu = CPU()
cpu.exec_all(lines)
print("Part 1:", cpu.signal_sum)

print("Part 2:")
print("\n".join(cpu.screen))
