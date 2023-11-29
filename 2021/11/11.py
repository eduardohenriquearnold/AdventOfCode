import numpy as np

def load(path):
    e = []
    with open(path, 'r') as f:
        for l in f.readlines():
            e.append([int(x) for x in l.strip()])
    return np.array(e)

def step(e):
    H, W = e.shape

    # increase enery of all octupus
    e += 1

    # check for flashes
    flashed = e > 9
    overall_flashed = flashed.copy()

    while flashed.sum() > 0:
        # add energy to neighbours of octupus that flashed
        idxs_flashed = np.nonzero(flashed)
        for i, j in zip(*idxs_flashed):
            for dx in (-1,0,1):
                for dy in (-1,0,1):
                    if 0<=(i+dy)<H and 0<=(j+dx)<W:
                        e[i+dy, j+dx] += 1

        # updates flashed mask
        flashed = np.logical_xor(overall_flashed, e>9)
        overall_flashed = np.logical_or(overall_flashed, e>9)
    
    # once flashing stops, reset energy of all flashed to 0
    e[overall_flashed] = 0

    total_flashes = overall_flashed.sum()
    return e, total_flashes

e = load('11/input.txt')
flashes = 0
i = 0
while(True):
    i += 1
    e, f = step(e)
    flashes +=f 
    if i == 100:
        print(flashes)
    
    if f == 100:
        print(i)
        break

