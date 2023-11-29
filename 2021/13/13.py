from typing import DefaultDict

def load(path):
    pts = []
    cmds = []
    with open(path, 'r') as f:
        for l in f.readlines():
            if ',' in l:
                x, y = l.strip().split(',')
                pts.append((int(x),int(y)))
            elif 'fold' in l:
                ax, n = l.strip().split('=')
                cmds.append((ax[-1], int(n)))
    return pts, cmds

def create_paper(pts):
    p = DefaultDict(int)
    for pt in pts:
        p[pt] = 1
    return p

def draw(p):
    H, W = 0, 0
    for x, y in p.keys():
        H = max(H, y)
        W = max(W, x)

    for i in range(H+1):
        line = []
        for j in range(W+1):
            c = ' ' if p[(j,i)] == 0 else '#'
            line.append(c)
        print(''.join(line))

def fold(p, cmd):
    '''fold paper (p) at (fold_pos) of axis (ax)'''

    ax, fold_pos = cmd
    d = 1 if ax == 'y' else 0
    fp = DefaultDict(int)

    for pos, v in p.items():
        if pos[d] > fold_pos and v == 1:
            new_pos = list(pos)
            new_pos[d] = 2*fold_pos - pos[d]
            fp[tuple(new_pos)] = 1
        elif v == 1:
            fp[pos] = 1
            
    return fp

pts, cmds = load('13/input.txt')
p = create_paper(pts)
# part 1
p1 = fold(p, cmds[0])
r1 = len(p)
print(r1)
# part 2
for cmd in cmds:
    p = fold(p, cmd)
draw(p)