from typing import DefaultDict

def sign(x):
    return (1, -1)[x<0]

def load(path):
    coords = []
    with open(path, 'r') as f:
        for line in f.readlines():
            c1, c2 = line.strip().split(' -> ')
            x1, y1 = c1.split(',')
            x2, y2 = c2.split(',')
            coords.append((int(x1), int(y1), int(x2), int(y2)))
    return coords

def fill_map(coords, diag=False):
    map = DefaultDict(int)
    for x1,y1,x2,y2 in coords:
        if x1 == x2:
            y1, y2 = min(y1, y2), max(y1,y2)
            for j in range(y1, y2+1, 1):
                map[(x1,j)] += 1
        elif y1 == y2:
            x1, x2 = min(x1, x2), max(x1,x2)
            for j in range(x1, x2+1, 1):
                map[(j,y1)] += 1
        elif diag:
            for x,y in zip(range(x1,x2+sign(x2-x1),sign(x2-x1)), range(y1,y2+sign(y2-y1),sign(y2-y1))):
                map[(x,y)] += 1
    return map

if __name__ == '__main__':
    coords = load('5/input.txt')
    map = fill_map(coords)
    r1 = sum([1 for v in map.values() if v >=2])
    map_diag = fill_map(coords, True)
    r2 = sum([1 for v in map_diag.values() if v >=2])
    print(f'Part1: {r1}')
    print(f'Part2: {r2}')
