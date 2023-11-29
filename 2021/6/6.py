from typing import DefaultDict

with open('6/input.txt', 'r') as f:
    fishes_start = list(map(int, f.readline().strip().split(',')))

# Part 1
fishes = fishes_start.copy()
days = 80
for _ in range(days):
    updated_fishes = fishes.copy()
    for i in range(len(fishes)):
        updated_fishes[i] -= 1

        # resets and add new fish
        if updated_fishes[i] == -1:
            updated_fishes[i] = 6
            updated_fishes.append(8)
    fishes = updated_fishes
r1 = len(fishes)
print(f'Part1: {r1}')

# Part 2 
# Exponential growth takes so much time - even if it's linear i.e. O(n)
# Let's create a map instead!
fishes = fishes_start.copy()
table = DefaultDict(int) # days left -> number of fish
for f in fishes:
    table[f] += 1

days = 256
for _ in range(days):
    updated_table = DefaultDict(int, {t-1:n for t,n in table.items() if t>=0})
    updated_table[8] = updated_table[-1]
    updated_table[6] += updated_table[-1]
    updated_table[-1] = 0
    table = updated_table

r2 = sum(table.values())
print(f'Part2: {r2}')