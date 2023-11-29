from copy import deepcopy

def countImediateOccupiedNeighbours(m, i, j):
    '''Count occupied seats adjacent to position (i,j) in map m'''

    occupied = 0
    for ii in [-1,0,1]:
        for jj in [-1,0,1]:
            if ii == 0 and jj == 0:
                continue
            if i+ii < 0 or i+ii>=len(m):
                continue
            if j+jj < 0 or j+jj>=len(m[0]):
                continue

            if  m[i+ii][j+jj] == '#':
                occupied += 1
    return occupied

def countExtendedOccupiedNeighbours(m, i, j):
    '''Count occupied seats adjacent to position (i,j) with extended neighbourhood (first seat that can be seen in each direction) in map m'''

    occupied = 0
    for di in [-1,0,1]:
        for dj in [-1,0,1]:
            if di == 0 and dj == 0:
                continue 
            ii = i + di
            jj = j + dj
            while (ii>=0 and ii<len(m) and jj>=0 and jj<len(m[0])):
                if m[ii][jj] != '.':
                    if m[ii][jj] == '#':
                        occupied += 1
                    break
                ii += di
                jj += dj
    return occupied

def process(m, countFunction, tolerance):
    '''map iteration process'''

    changes = 0
    um = deepcopy(m)

    for i in range(len(m)):
        for j in range(len(m[0])):
            x = m[i][j]
            if x == '.':
                continue
            occ = countFunction(m, i, j)
            if x == 'L' and occ == 0:
                um[i][j] = '#'
                changes += 1
            elif x == '#' and occ >= tolerance:
                um[i][j] = 'L'
                changes += 1
    return changes, um

def countOccupied(m):
    '''count all occupied seats in a map'''
    occ = 0
    for l in m:
        for s in l:
            if s == '#':
                occ += 1
    return occ

#Load map (2d array)
_m = [list(l.rstrip('\n')) for l in open('./inputs/11', 'r')]

#P1: uses imediate neighbours function
m = deepcopy(_m)
changes = 1
while (changes>0):
    changes, m = process(m, countImediateOccupiedNeighbours, 4)
print(f'P1: number of occupied seats is {countOccupied(m)}')

#P2: uses extended neighbourhood function
m = deepcopy(_m)
changes = 1
while (changes>0):
    changes, m = process(m, countExtendedOccupiedNeighbours, 5)
print(f'P2: number of occupied seats is {countOccupied(m)}')
