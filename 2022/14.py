from collections import defaultdict

ROCK = "#"
SAND = "o"
EMPTY = ""


def parse_input(path):
    cave = defaultdict(str)

    with open(path, "r") as f:
        for line in f.readlines():
            traces = line.strip().split(" -> ")
            traces = [tuple(map(int, trace.split(","))) for trace in traces]
            for (x0, y0), (x1, y1) in zip(traces[:-1], traces[1:]):
                if x0 == x1:
                    miny, maxy = min(y0, y1), max(y0, y1)
                    for y in range(miny, maxy + 1):
                        cave[(x0, y)] = "#"
                elif y0 == y1:
                    minx, maxx = min(x0, x1), max(x0, x1)
                    for x in range(minx, maxx + 1):
                        cave[(x, y0)] = "#"
                else:
                    raise RuntimeError("Unexpected input")

    return cave


def get_lowest_rock(cave):
    return max([y for (_, y), item in cave.items() if item == ROCK])


def pour_sand(cave: dict, lowest_rock: int, hole: tuple = (500, 0), infinite_floor=False) -> bool:
    """Pours sand into cave. Returns True if new sand is detained; False if sand falls to void"""

    pos = list(hole)
    while True:
        found_empty = False
        for delta in ((0, 1), (-1, 1), (1, 1)):
            new_pos = [v + d for v, d in zip(pos, delta)]
            item = cave[tuple(new_pos)]
            if infinite_floor and new_pos[1] == lowest_rock + 2:
                item = ROCK

            if item == EMPTY:
                found_empty = True
                break

        if found_empty:
            pos = new_pos
        else:
            cave[tuple(pos)] = SAND
            return True

        if pos[1] > lowest_rock and not infinite_floor:
            return False


def print_cave(cave):
    xs = [x for (x, _) in cave.keys()]
    ys = [y for (_, y) in cave.keys()]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)

    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            item = cave[x, y]
            item = "." if item == "" else item
            print(item, end="")
        print()


cave = parse_input("inputs/14.txt")
lowest_rock = get_lowest_rock(cave)

# P1
pours = 0
while pour_sand(cave, lowest_rock):
    pours += 1
print(pours)

# P2
while cave[(500, 0)] != SAND:
    pour_sand(cave, lowest_rock, infinite_floor=True)
    pours += 1
print(pours)
