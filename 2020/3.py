#part 1
trees = 0
xCoord = 0
for l in open('./inputs/3', 'r').readlines():
    xCoord = xCoord % (len(l)-1)
    if l[xCoord] == '#':
        trees += 1
    xCoord += 3
print(f'P1: Total trees found: {trees}')

#part 2
def countTrees(sr, sd):
    '''Count the number of trees with slope right and slope down'''
    trees = 0
    xCoord = 0
    yCoord = 0
    for y, l in enumerate(open('./inputs/3', 'r').readlines()):
        if y != yCoord:
            continue

        xCoord = xCoord % (len(l)-1)
        if l[xCoord] == '#':
            trees += 1
        xCoord += sr
        yCoord += sd
    return trees
    
res = countTrees(1,1) * countTrees(3,1) * countTrees(5,1) * countTrees(7,1) * countTrees(1,2)
print(f'P2: Result: {res}')