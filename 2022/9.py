from math import sqrt


def clip(c: complex) -> complex:
    """Returns complex where real and imag. parts are the signs of original complex."""
    real = c.real / abs(c.real) if c.real != 0 else 0
    imag = c.imag / abs(c.imag) if c.imag != 0 else 0
    return complex(real, imag)


class Rope:
    def __init__(self, length: int) -> None:
        self.knots = [complex()] * length
        self.tail_history = set()

    def move_head(self, direction: str, quantity: int):
        axis_directions = {"U": 1j, "D": -1j, "R": 1, "L": -1}
        assert direction in axis_directions.keys(), "invalid direction"

        for _ in range(quantity):
            self.knots[0] += axis_directions[direction]
            self.update_knots()

    def update_knots(self):
        for i in range(1, len(self.knots)):
            diff = self.knots[i - 1] - self.knots[i]

            if abs(diff) > sqrt(2):
                self.knots[i] += clip(diff)

        self.tail_history.add(self.knots[-1])

    def tail_history_length(self) -> int:
        return len(self.tail_history)


rope2 = Rope(length=2)
rope10 = Rope(length=10)
for line in open("inputs/9.txt", "r").readlines():
    direction, step = line.strip().split(" ")
    step = int(step)

    rope2.move_head(direction=direction, quantity=int(step))
    rope10.move_head(direction=direction, quantity=int(step))

print(rope2.tail_history_length())
print(rope10.tail_history_length())
