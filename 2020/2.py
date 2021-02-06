import re

r = re.compile('([0-9]+)-([0-9]+) ([a-z]): ([a-z]+$)')

#Part One
valid = 0
for l in open('./inputs/2', 'r').readlines():
    groups = r.match(l)
    _, minC, maxC, letter, passw = [groups.group(i) for i in range(5)]
    minC, maxC = int(minC), int(maxC)

    count = 0
    for c in passw:
        if c == letter:
            count += 1
    
    if count >= minC and count <= maxC:
        valid +=1

print(f'P1: Number of valid password: {valid}')

#Part Two
valid = 0
for l in open('./inputs/2', 'r').readlines():
    groups = r.match(l)
    _, idx1, idx2, letter, passw = [groups.group(i) for i in range(5)]
    idx1, idx2 = int(idx1)-1, int(idx2)-1
    
    if (passw[idx1] == letter) != (passw[idx2] == letter):
        valid +=1

print(f'P2: Number of valid password: {valid}')