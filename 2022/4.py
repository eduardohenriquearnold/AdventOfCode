from __future__ import annotations


class Assignment:
    def __init__(self, code: str) -> None:
        self.id0, self.id1 = map(int, code.strip().split("-"))

    def fully_overlaps(self, another: Assignment) -> bool:
        if self.id0 >= another.id0 and self.id0 <= another.id1 and self.id1 >= another.id0 and self.id1 <= another.id1:
            return True
        return False

    def overlaps(self, another: Assignment) -> bool:
        if (self.id0 >= another.id0 and self.id0 <= another.id1) or (
            self.id1 <= another.id1 and self.id1 >= another.id0
        ):
            return True
        return False


full_overlaps = 0
overlaps = 0
for line in open("inputs/4.txt", "r").readlines():
    pair = line.strip().split(",")
    assert len(pair) == 2, "expected pair of assignments"

    a0, a1 = map(Assignment, pair)

    if a0.fully_overlaps(a1) or a1.fully_overlaps(a0):
        full_overlaps += 1
    if a0.overlaps(a1) or a1.overlaps(a0):
        overlaps += 1

print(full_overlaps)
print(overlaps)
