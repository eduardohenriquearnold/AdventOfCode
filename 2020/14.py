import re
from itertools import chain, combinations

maskRE = re.compile('mask = ([0,1,X]{36})')
memRE = re.compile('mem\[([0-9]+)\] = ([0-9]+)')

#P1: load values to memory
mem = {}
for line in open('./inputs/14'):
    if match := maskRE.match(line):
        mask = [(2**(35-pos), int(b)) for (pos,b) in enumerate(match.group(1)) if b != 'X']
    elif match := memRE.match(line):
        addr, val = map(int, match.group(1,2))
        for (n,b) in mask:
            nval = n & val
            if b == 0:
                val = val - nval if nval > 0 else val
            elif b == 1:
                val = val + n if nval == 0 else val
        mem[addr] = val
print(f'P1: Sum of memory values: {sum(mem.values())}')

#P2: decoder version 2
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

mem = {}
for line in open('./inputs/14'):
    if match := maskRE.match(line):
        mask = match.group(1)
        dontCare = [2**(35-i) for (i,c) in enumerate(mask) if c == 'X']
        mask = int(mask.replace('X','0'), 2)
    elif match := memRE.match(line):
        addr, val = map(int, match.group(1,2))
        addr |= mask
        #Remove 1's from addr if there's a dont care at that position
        for n in dontCare:
            addr -= n if n & addr > 0 else 0
        
        #Check all combinations of dontcares (binary tree)
        for p in powerset(dontCare):
            mem[addr + sum(p)] = val
print(f'P2: Sum of memory values: {sum(mem.values())}')
