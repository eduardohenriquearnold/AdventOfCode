def priority(char: str) -> int:
    """Maps single char to integer.

    a-z mapped to 1-26
    A-Z mapped to 27-52
    """
    assert len(char) == 1, "only a single letter allowed"
    out = ord(char)

    if out > 90:
        out -= 96
    else:
        out -= 38

    return out


def part1(lines):
    out = 0
    for line in lines:
        line = line.strip()
        csize = len(line) // 2
        c0, c1 = line[:csize], line[csize:]

        intersection = set(c0).intersection(c1)
        assert len(intersection) == 1, "more than one item repeated in compartments"
        out += priority(intersection.pop())
    print(out)


def part2(lines):
    lines = [l.strip() for l in lines]

    out = 0
    for elf0, elf1, elf2 in zip(lines[::3], lines[1::3], lines[2::3]):
        common_item = set(elf0).intersection(set(elf1), set(elf2))
        assert len(common_item) == 1, "more than one item repeated across elfs"
        out += priority(common_item.pop())
    print(out)


lines = open("inputs/3.txt", "r").readlines()
part1(lines)
part2(lines)
