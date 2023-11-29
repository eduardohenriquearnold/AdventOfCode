import re
from collections import defaultdict

#Detect all possible patterns
rule = re.compile(r'w|e|nw|ne|se|sw')

tiles = defaultdict(int) #0 is white, 1 black
MOVEMENTS = {'w':[1,0], 'nw':[0.5, 0.5], 'ne':[-0.5,0.5], 'e':[-1,0], 'se':[-0.5,-0.5], 'sw':[0.5,-0.5]}

for l in open('./inputs/24','r'):
    pos = [0,0]
    for tile in rule.findall(l):
        mov = MOVEMENTS[tile]
        pos[0] += mov[0]
        pos[1] += mov[1]
    tiles[tuple(pos)] = 1 - tiles[tuple(pos)]

blacks = sum(tiles.values())
print(f'P1: number of tiles with black on top is {blacks}')


#Part 2 
def countBlackNeighbours(tiles, tilekey):
    blackNeigh = 0
    for dkey in MOVEMENTS.values():
        k = (tilekey[0] + dkey[0], tilekey[1] + dkey[1])
        blackNeigh += 1 if k in tiles and tiles[k] == 1 else 0
    return blackNeigh

def process(tiles):
    flip = []
    for key, val in tiles.items():
        bn = countBlackNeighbours(tiles, key)
        if val == 1 and (bn == 0 or bn > 2):
            flip.append(key)
        elif val == 0 and bn == 2:
            flip.append(key)
            
    #Flip tiles
    for key in flip:
        tiles[key] = 1 - tiles[key]
        
    return tiles

def fillNeighbours(tiles):
    '''Ensures that all tiles have neighbours'''
    keysToAdd = []
    for key in tiles.keys():
        for dkey in MOVEMENTS.values():
            k = (key[0] + dkey[0], key[1] + dkey[1])
            if k not in tiles:
                keysToAdd.append(k)
    
    for k in keysToAdd:
        tiles[k] = 0
    return tiles

for _ in range(100):
    tiles = fillNeighbours(tiles)
    tiles = process(tiles)
blacks = sum(tiles.values())
print(f'P2: number of tiles with black on top is {blacks}')