# Part 1
with open('input.txt', 'r') as f:
    h, d = 0, 0
    for line in f.readlines():
        cmd, x = line.rstrip().split(' ')
        x = int(x)

        if cmd == 'forward':
            h += x
        elif cmd == 'down':
            d += x
        elif cmd == 'up':
            d -= x
print(f'Part 1: {h*d}')

# Part 2
with open('input.txt', 'r') as f:
    h, d, a = 0, 0, 0
    for line in f.readlines():
        cmd, x = line.rstrip().split(' ')
        x = int(x)

        if cmd == 'forward':
            h += x
            d += a * x
        elif cmd == 'down':
            a += x
        elif cmd == 'up':
            a -= x
print(f'Part 2: {h*d}')

