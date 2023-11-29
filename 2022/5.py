from collections import deque, defaultdict, namedtuple
import copy

Command = namedtuple("Command", ("quantity", "src", "dst"))


def load(lines: list[str]) -> tuple[dict[int, deque], list[Command]]:
    sup = defaultdict(deque)
    cmds = list()

    for line in lines:
        line = line.rstrip()

        if "[" in line:
            for i, crate in enumerate(line[i] for i in range(1, len(line), 4)):
                if crate != " ":
                    sup[i].append(crate)

        if "move" in line:
            args = line.split(" ")
            cmds.append(Command(quantity=int(args[1]), src=int(args[3]) - 1, dst=int(args[5]) - 1))

    # reverse supply crates (we loaded them in inverse order)
    for stack in sup.values():
        stack.reverse()

    return sup, cmds


def get_letters(sup):
    """Sort supply according to stack id and return crates on top, if non-empty"""
    sup = {id: sup[id] for id in range(len(sup))}
    letters = "".join([stack.pop() for stack in sup.values() if len(stack) > 0])
    print(letters)


def part1(sup, cmds):
    for cmd in cmds:
        for _ in range(cmd.quantity):
            crate = sup[cmd.src].pop()
            sup[cmd.dst].append(crate)
    get_letters(sup)


def part2(sup, cmds):
    for cmd in cmds:
        current_move = []
        for _ in range(cmd.quantity):
            crate = sup[cmd.src].pop()
            current_move.append(crate)
        sup[cmd.dst].extend(current_move[::-1])
    get_letters(sup)


lines = open("inputs/5.txt", "r").readlines()
sup, cmds = load(lines)

part1(copy.deepcopy(sup), cmds)
part2(copy.deepcopy(sup), cmds)
