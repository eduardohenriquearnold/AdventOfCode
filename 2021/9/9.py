def load(path):
    h = []
    with open(path, 'r') as f:
        for l in f.readlines():
            h.append([int(x) for x in l.strip()])
    return h 

def low_pts(h):
    '''return i,j indices of low points'''
    H, W = len(h), len(h[0])
    idxs = []
    for i in range(H):
        for j in range(W):
            neigh = 0
            smaller = 0
            cur = h[i][j]
            if i-1 >= 0:
                neigh += 1
                smaller += 1 if h[i-1][j] > cur else 0
            if i + 1 < H:
                neigh += 1
                smaller += 1 if h[i+1][j] > cur else 0
            if j - 1 >= 0:
                neigh += 1
                smaller += 1 if h[i][j-1] > cur else 0
            if j + 1 < W:
                neigh += 1
                smaller += 1 if h[i][j+1] > cur else 0
            if neigh == smaller:
                idxs.append((i,j))
    return idxs

def size_basin(h, pt):
    H, W = len(h), len(h[0])
    stack = [pt]
    size = 0

    while len(stack) > 0:
        i, j = stack.pop()
        if i>=H or i < 0 or j >= W or j < 0:
            continue
        if h[i][j] == 9:
            continue
        size += 1
        h[i][j] = 9 # avoid re-starting here again
        stack.append((i+1,j))
        stack.append((i-1,j))
        stack.append((i,j+1))
        stack.append((i,j-1))
    return size

def part1(h):
    idxs = low_pts(h)
    s = sum([h[i][j] + 1 for (i,j) in idxs])
    return s

def part2(h):
    idxs = low_pts(h)
    basin_sizes = sorted([size_basin(h, pt) for pt in idxs])
    return basin_sizes[-3] * basin_sizes[-2] * basin_sizes[-1]

h = load('9/input.txt')
print(part1(h))
print(part2(h))

