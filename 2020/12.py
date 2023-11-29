# Part 1
x, y = 0, 0
d = 0
for line in open("./inputs/12", "r"):
    c = line[0]
    val = int(line[1:])
    if c == "N":
        y += val
    elif c == "S":
        y -= val
    elif c == "E":
        x += val
    elif c == "W":
        x -= val
    elif c == "R":
        d += val
    elif c == "L":
        d -= val
    elif c == "F":
        d = d % 360

        if d == 0:
            x += val
        elif d == 90:
            y -= val
        elif d == 180:
            x -= val
        elif d == 270:
            y += val
        else:
            raise Exception("Invalid angle")
    else:
        raise Exception("Invalid command")
print(f"P1: x={x} y={y}. Manhattan distance={abs(x)+abs(y)}")

# Part 2
x, y = 0, 0
wx, wy = 10, 1
for line in open("./inputs/12", "r"):
    c = line[0]
    val = int(line[1:])
    if c == "N":
        wy += val
    elif c == "S":
        wy -= val
    elif c == "E":
        wx += val
    elif c == "W":
        wx -= val
    elif c == "R":
        for r in range(0, val, 90):
            wx, wy = wy, -wx
    elif c == "L":
        for r in range(0, val, 90):
            wx, wy = -wy, wx
    elif c == "F":
        x += val * wx
        y += val * wy
    else:
        raise Exception("Invalid command")
print(f"P2: x={x} y={y}. Manhattan distance={abs(x)+abs(y)}")
