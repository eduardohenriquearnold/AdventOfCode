class LinkedListNode:
    def __init__(self, v, p, n):
        '''v is value, p in previous, n is next'''
        self.v = v
        self.p = p
        self.n = n

class LinkedList:
    '''Cyclic Linked list with dictionary for O(1) lookups'''

    def __init__(self, it):
        '''Creates a linked list given a list '''
        self.map = {}

        #First element
        first = LinkedListNode(it[0], None, None)
        self.map[it[0]] = first
        cur = first

        #Add all elements
        for v in it[1:]:
            nex = LinkedListNode(v, cur, None)
            cur.n = nex
            self.map[v] = nex
            cur = nex

        #Connect last and first elements
        cur.n = first
        first.p = cur
        self.first = first

    def __getitem__(self, key):
        '''Return Node with given value. Assume nodes values are static'''
        return self.map[key]

def move(cups, current, mincup, maxcup):
    '''cups is LinkedList, current is LinkedListNode, mincup and maxcup are the min/max cup labels respectively'''

    #get picked cups
    pick1 = current.n
    pick2 = pick1.n
    pick3 = pick2.n

    #get selected cup
    vsel = current.v - 1
    while vsel in [pick1.v, pick2.v, pick3.v] or vsel < mincup:
        vsel -= 1
        if vsel < mincup:
            vsel = maxcup
    sel = cups[vsel]

    #remove [pick1,pick2,pick3] from current ... next
    current.n = pick3.n
    (pick3.n).p = current

    #move [pick1,pick2,pick3] to immediately after sel: [..., sel, pick1, pick2, pick3, ...]
    pick1.p = sel
    pick3.n = sel.n
    sel.n, (sel.n).p = pick1, pick3

    return current.n

#P1
label = '318946572'
cups = LinkedList([int(l) for l in label])
cur = cups.first
for _ in range(100):
    cur = move(cups, cur, 1, 9)
cur = cups[1].n
ans = []
while True:
    if cur.v == 1:
        break
    ans.append(cur.v)
    cur = cur.n
ans = "".join(map(str, ans))
print(f'P1: {ans}')

#P2
cups = [int(l) for l in label] + list(range(10,10**6+1))
cups = LinkedList(cups)
cur = cups.first
for _ in range(10**7):
    cur = move(cups, cur, 1, 10**6)
cur = cups[1].n
ans = cur.v * cur.n.v
print(f'P2: {ans}')