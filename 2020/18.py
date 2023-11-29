def parseEx(ex):
    '''Transform str expression into a computation graph in a list'''
    graph = []
    pointer = [graph]
    for x in ex:
        if x == ' ' or x == '\n':
            continue
        if x == '(':
            pointer[0].append([])
            pointer.insert(0, pointer[0][-1])
        elif x == ')':
            pointer.pop(0)
        elif x in ['+','*']:
            pointer[0].append(x)
        else:
            try:
                x = int(x)
                pointer[0].append(x)
            except ValueError:
                print('Invalid expression!')
    return graph

def executeGraph(g):
    '''Executes computation graph considering same precedence between sum and multiplication'''

    op = None
    res = None
    for e in g:
        if type(e) == str:
            op = e
        elif type(e) == list:
            e = executeGraph(e)
        if type(e) == int:
            if op == None:
                res = e
            else:
                res = res + e if op == '+' else res * e
    return res

def changePrecedence(g):
    '''Transforms a graph to consider sum preceding multiplication'''

    ng = []
    i = 0
    while i < len(g):
        e = g[i]
        if type(e) == list:
            ng.append(changePrecedence(e))
        elif e == '+':
            next = changePrecedence(g[i+1]) if type(g[i+1])==list else g[i+1]
            ng[-1] = [ng[-1],'+',next]
            i += 1
        else:
            ng.append(e)
        i += 1
    return ng


#P1 - same precedence
s = 0
for ex in open('./inputs/18','r'):
    g = parseEx(ex)
    s += executeGraph(g)
print(f'P1: sum of results is {s}')

#P2 - sum precede multiplication
s = 0
for ex in open('./inputs/18','r'):
    g = parseEx(ex)
    g = changePrecedence(g)
    s += executeGraph(g)
print(f'P2: sum of results is {s}')
