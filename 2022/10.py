class Command:
    def __init__(self, cycles: int):
        self.cycles = cycles

    def execute(self, cpu):
        pass


class CommandNOOP(Command):
    def __init__(self) -> None:
        super().__init__(cycles=1)


class CommandADDX(Command):
    def __init__(self, value) -> None:
        super().__init__(cycles=2)
        self.value = value

    def execute(self, cpu):
        cpu.x += self.value


class CPU:
    def __init__(self, cmds) -> None:
        self.cmds = cmds
        self.x = 1
        self.cycles = 0
        self.crt = []

    def cycle(self) -> None:
        if self.cmds[0].cycles == 0:
            self.cmds.pop(0).execute(self)

        self.cycles += 1
        if len(self.cmds) > 0:
            self.cmds[0].cycles -= 1

        self.draw_crt()

    def draw_crt(self) -> None:
        CRT_WIDTH = 40
        pixel = "#" if abs((self.cycles - 1) % CRT_WIDTH - self.x) <= 1 else "."
        self.crt.append(pixel)

        if self.cycles % CRT_WIDTH == 0:
            self.crt.append("\n")

    def has_work(self) -> bool:
        return len(self.cmds) > 0


def parse_cmds(lines):
    cmds = []
    for line in lines:
        if "noop" in line:
            cmds.append(CommandNOOP())
        elif "addx" in line:
            val = int(line.strip().split(" ")[1])
            cmds.append(CommandADDX(value=val))
        else:
            raise RuntimeError("Invalid command")
    return cmds


cmds = parse_cmds(open("inputs/10.txt", "r").readlines())
cpu = CPU(cmds=cmds)
cycles_interest = tuple(range(20, 260, 40))
strength = {}

while cpu.has_work():
    cpu.cycle()
    if cpu.cycles in cycles_interest:
        strength[cpu.cycles] = cpu.x

p1 = sum((i * j for i, j in strength.items()))
p2 = "".join(cpu.crt)
print(p1)
print(p2)
