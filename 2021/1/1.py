with open('input.txt', 'r') as f:
    numbers = [int(l.rstrip()) for l in f.readlines()]

# part 1
greater = 0
for d0, d1 in zip(numbers[:-1], numbers[1:]):
    greater += 1 if d1 > d0 else 0

print(f'part 1: {greater}')

# part 2
greater = 0
prev_s = 100000
for d0, d1, d2 in zip(numbers[:-2], numbers[1:-1], numbers[2:]):
    s = d0 + d1 + d2
    greater += 1 if s > prev_s else 0
    prev_s = s

print(f'part 2: {greater}')

