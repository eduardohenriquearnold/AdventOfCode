#Load list
l = [int(n.rstrip('\n')) for n in open('./inputs/10', 'r')]
l.sort()

#add first and last elements
l.insert(0,0) #outlet
l.append(l[-1]+3) #laptop

#P1 count differences
d1 = 0
d3 = 0
for i in range(len(l)-1):
    d = l[i+1] - l[i]
    if d == 1:
        d1 +=1
    elif d == 3:
        d3 += 1
print(f'P1: differences of 1 were {d1}; differences of 3 were {d3}; the product is {d1*d3}')

#P2 counting arrangements -- ineficient way with recursion
l = [int(n.rstrip('\n')) for n in open('./inputs/10', 'r')]
l.sort()
l.insert(0,0)

def genSequence(seq, adaptors):
    if len(seq) == 0:
        seq = [adaptors[-1]]

    if seq[0] == 0:
        yield seq

    for i in range(len(adaptors)-1-len(seq), -1, -1):
        if seq[0] - adaptors[i] <= 3 and adaptors[i] < seq[0]:
            yield from genSequence([adaptors[i]]+seq, adaptors)

print(l)
count = 0
# for s in genSequence([], l):
    # count += 1
print(f'P2: number of possibilities: {count}')

#P2 faster way -- with Dynamic programming
l = [0,3,4,5,6]
from collections import defaultdict
pos = defaultdict(int)
pos[l[-1]]=1
for i in l[-2::-1]:
    pos[i]=pos[i+1]+pos[i+2]+pos[i+3]
print(f'P2: number of possibilities {pos[0]}')



