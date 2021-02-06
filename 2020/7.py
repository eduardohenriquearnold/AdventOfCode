#Load data into graph
#bags Dict: key is the bag name, value is a list of lists [[name1,name2,name3], [qty1, qty2, qty3]]
bags = {} 
for rule in open('./inputs/7', 'r'):
    #get bag name
    idx = rule.find(' bags')
    bname = rule[:idx]

    #empty bag
    if rule.find('no other bags') > 0:
        names = []
        qtys = []
    else:
        #non-empty bag: get content's name and quantity for each bag
        idx = rule.find('contain')
        contents = rule[idx+7:].replace(' bags','').replace(' bag','').rstrip('.\n')
        contents = contents.split(',')
        names = [c[3:] for c in contents]
        qtys = [int(c[1]) for c in contents]

    #add to dictionary, creating a graph structure indexed by the bag name
    bags[bname] = [names,qtys]

#Part 1: Iterate to check how many possibilities to get a shiny gold bag
ways = 0
for b, content in bags.items():
    todo = content[0].copy()
    while (len(todo) > 0):
        cur = todo.pop()
        if cur == 'shiny gold':
            ways += 1
            break
        todo += bags[cur][0]
print(f'P1: possible ways to carry shiny gold: {ways}')

#Part 2: Check how many bags inside a shiny gold bag
def nbags(bname):
    '''Recursively iterate to obtain number of bags within a given bag'''
    n = 0
    for name, qty in zip(*bags[bname]):
        n += qty + qty * nbags(name)
    return n
nShinyGold = nbags('shiny gold')
print(f'Number of bags inside a shiny gold bag: {nShinyGold}')