from collections import defaultdict
from math import prod

import numpy as np
from scipy.signal import convolve2d

def getHash(tile, both=True):
    '''Returns hash from all tiles borders, hash is the max number that could be formed using the borders as binary encoded numbers, reading from direct (top->bottom or left->right) or inverse order.
    The border order is: left,bottom,right,top'''

    direct = 2**np.arange(tile.shape[0])
    inverse = direct[::-1]

    hashes = []
    for border in [tile[:,0], tile[-1,:], tile[:,-1], tile[0,:]]:
        if both:
            hashes.append(max(np.sum(direct*border), np.sum(inverse*border)))
        else:
            hashes.append(np.sum(direct*border))
    return hashes

def rotate(tile):
    '''Rotate tile by 90deg clockwise'''
    return tile.copy().T[:,::-1]

#Load tiles
tiles = defaultdict(list)
for l in open('./inputs/20','r'):
    if 'Tile' in l:
        cur = int(l[-6:-2])
    elif l == '\n':
        tiles[cur] = np.array(tiles[cur]).astype(np.int)
    else:
        tiles[cur].append(list(l.rstrip().replace('#','1').replace('.','0')))

#Get hash for all tiles borders
hashes = {}
for i,t in tiles.items():
    hashes[i] = getHash(t)

#Count hashes over all tiles
cHashes = defaultdict(int)
for hs in hashes.values():
    for h in hs:
        cHashes[h] += 1

#Part 1 results
#Get tiles that has exactly 2 borders with 2 counts (counts = 2,2,1,1)
sTiles = [i for i,c in hashes.items() if sum([cHashes[j] for j in c])==6]
print(f'P1: product of corner tiles\' ids is {prod(sTiles)}')

#Part 2
#create dict that give the tile ID's that contain a given hash
tileContaining = defaultdict(list)
for i,t in tiles.items():
    for h in getHash(t):
        tileContaining[h].append(i)

#get ID's and correct rotation/flipping
tilesInRow = int(len(tiles)**0.5)
ids = np.zeros((tilesInRow,tilesInRow),dtype=np.int)

#First tile is a corner one, but need to adjust to the right orientation
ids[0,0] = sTiles[0]
while [cHashes[b] for b in getHash(tiles[ids[0,0]])] != [1,2,2,1]:
        tiles[ids[0,0]] = rotate(tiles[ids[0,0]])
#remove hashes from tileContaining
for h in getHash(tiles[ids[0,0]]):
    tileContaining[h].remove(ids[0,0])

#construct the whole list of ids, rotating/flipping to match adjacent tiles
i,j = 0,1
while i<tilesInRow:
    while j<tilesInRow:
        if j == 0:
            #set current tile ID, based on previous tile border on the top. remove current id from tileContaining
            lastTileHashes = getHash(tiles[ids[i-1,j]])
            ids[i,j] = tileContaining[lastTileHashes[1]].pop()
            for h in getHash(tiles[ids[i,j]]):
                try:
                    tileContaining[h].remove(ids[i,j])
                except ValueError: pass

            #adjust rotation
            while getHash(tiles[ids[i,j]])[3] != lastTileHashes[1]:
                tiles[ids[i,j]] = rotate(tiles[ids[i,j]])

            #adjust flipping
            if getHash(tiles[ids[i-1,j]], False)[1] != getHash(tiles[ids[i,j]], False)[3]:
                tiles[ids[i,j]] = tiles[ids[i,j]][:,::-1]
        else:
            #set current tile ID, based on previous tile border on the left. remove current id from tileContaining
            lastTileHashes = getHash(tiles[ids[i,j-1]])
            ids[i,j] = tileContaining[lastTileHashes[2]][0]
            for h in getHash(tiles[ids[i,j]]):
                try:
                    tileContaining[h].remove(ids[i,j])
                except ValueError: pass

            #adjust rotation
            while getHash(tiles[ids[i,j]])[0] != lastTileHashes[2]:
                tiles[ids[i,j]] = rotate(tiles[ids[i,j]])

            #adjust flipping
            if getHash(tiles[ids[i,j-1]], False)[2] != getHash(tiles[ids[i,j]], False)[0]:
                tiles[ids[i,j]] = tiles[ids[i,j]][::-1,:]
        j += 1
    j = 0
    i += 1

#Assemble the whole image by concatenating IDS (and removing borders)
img = np.concatenate([np.concatenate([tiles[ids[i,j]][1:-1,1:-1] for j in range(tilesInRow)], axis=1) for i in range(tilesInRow)], axis=0)

#Define sea monster pattern
pattern = np.array(list('                  # #    ##    ##    ### #  #  #  #  #  #   '.replace('#','1').replace(' ','0')), dtype=np.int).reshape(3,-1)

#Invert and rotate image
img = img[::-1]
img = rotate(rotate(img))

#Find sea monsters using 2d convolution of the pattern with the image
res = convolve2d(img, pattern, mode='valid') == pattern.sum()
nMonsters = res.sum()

#compute Roughness as the number of #(1's) in the image, minus the # in all sea monsters
roughness = img.sum() - pattern.sum() * nMonsters
print(f'P2: Found {nMonsters}. Sea roughness is {roughness}')