from math import ceil

#Load data
time, buses = open('./inputs/13', 'r').readlines()
time = int(time)
validBuses = [int(b) for b in buses.split(',') if b != 'x']

#Part 1
bestWait = time
busID = -1
for b in validBuses:
    wait = ceil(time/b) * b - time
    if wait < bestWait:
        bestWait = wait
        busID = b
print(f'P1: Bus {busID}, needs waiting {bestWait}. Res {busID*bestWait}')

#Part 2
#create list of (pos,id)
schedule = [(i,int(id)) for (i,id) in enumerate(buses.split(',')) if id != 'x']

'''
Given 2 prime numbers: a,b
Once we find a multiple of a that is within a k-distance from a multiple of b, this pattern will repeat every b multiples of a.

E.g.

3   7
6  14
9  21
12 28
15 35
18
21
24
27
30
33

using k=2, the first match is at 12 and 14 (because 12 + 2 = 14)
The same happens on the next 7th multiple of 3: 33 and 35 (note that 35 is the 3rd multiple).
This pattern repeats indefinetely.
'''

skip = schedule[0][1]
n = schedule[0][0] + skip
for (delay, bid) in schedule[1:]:
    while (n + delay) % bid != 0:
        n += skip
    skip *= bid    

print(f'P2: {n}')