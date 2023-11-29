#Load list
l = [int(n.rstrip('\n')) for n in open('./inputs/9', 'r')]

#P1 - Check for outlier
def isValid(preamble, value):
    '''Check if value is a valid sum of any element in preamble'''

    p = preamble.copy()
    p.sort()
    i = 0
    j = len(preamble)-1
    while (i != j):
        s = p[i] + p[j]
        if s > value:
            j -= 1
        elif s < value:
            i += 1
        else:
            return True
    return False

pl = 25 #length of preamble
for i in range(pl,len(l)):
    pre = l[i-pl:i]
    v = l[i]
    if not isValid(pre, v):
        print(f'P1: outlier found: {v}')
        break

#P2 - Finding a contiguous set that sum to the outlier value (v) 

#create integral list
il = [sum(l[:i]) for i in range(len(l))]

#search for interval that sums to v. O(n^2)
for i in range(len(il)):
    for j in range(i+2,len(il)):
        s = il[j] - il[i]
        if s == v:
            interval = l[i:j]
            print(f'Found interval! min={min(interval)} max={max(interval)} encryption weakness={min(interval)+max(interval)}')