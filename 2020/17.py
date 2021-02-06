import numpy as np
import itertools

def activeNeigh(c,*argv) -> int:
    '''Get number of active neighbours for arbitrary number of dimensions'''
    assert len(c.shape) == len(argv), 'number of coordinates must match the number of dimensions of cube'

    active = 0
    ndim = len(argv)
    neigh = [[-1,0,1]]*ndim
    for didxs in itertools.product(*neigh):
        if didxs ==(0,)*ndim:
            continue

        idxs = [i+di for (i,di) in zip(argv,didxs)]
        for i,shape in zip(idxs,c.shape):
            if i<0 or i>=shape:
                break
        else:
            active += c[tuple(idxs)]
    return active

def cycle(c) -> np.array:
    '''Executes one simulation cycle on the given cube of arbitrary dimension'''

    #adds external border
    c = np.pad(c, 1)
    nc = c.copy()

    #check all cells
    it = np.nditer(c, flags=['multi_index'], op_flags=['readonly'])
    for x in it:
        idx = it.multi_index
        active = activeNeigh(c, *idx)
        if x == 1:
            nc[idx] = 1 if active==2 or active==3 else 0
        else:
            nc[idx] = 1 if active==3 else 0
    return nc

#Load cube from memory. shape [Z,X,Y]
c = [list(map(int, l.rstrip().replace('#','1').replace('.','0'))) for l in open('./inputs/17','r').readlines()]
c = np.array(c)[np.newaxis,:,:]

#Part 1
c1 = c.copy()
for _ in range(6):
    c1 = cycle(c1)
print(f'P1: After 6 cycles the number of active elements is: {c1.sum()}')

#Part 2
c2 = c.copy()[np.newaxis,:,:,:]
for _ in range(6):
    c2 = cycle(c2)
print(f'P2: After 6 cycles the number of active elements is: {c2.sum()}')
