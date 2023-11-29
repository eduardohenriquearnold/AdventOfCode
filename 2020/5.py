def decode(b0, b1, s):
    '''Decode string given by binary numbers encoded by binary 0 and binary 1 characters into decimal.
        E.g. decode("L","H","HLH") -> 101 (binary) -> 5 (decimal) '''

    s = s.replace(b0, '0').replace(b1,'1')
    return int(s, 2)

seatList = []
maxID = 0
for l in open('./inputs/5', 'r'):
    row = decode('F','B',l[:7])
    col = decode('L','R',l[7:])
    i = 8*row + col
    maxID = max(maxID, i)
    seatList.append(i)
print(f'P1: Max ID: {maxID}')

#Part 2, finding my seat
for i in range(1024):
    if i not in seatList:
        print(f'P2: {i} not in the list!')