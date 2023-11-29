import numpy as np

#load
n = np.loadtxt('./inputs/1', dtype=np.int32)

#sort
n.sort()

#Part 1: find sum of 2 numbers == 2020. O(n)
i, j = 0, len(n)-1
while i != j:
    s = n[i] + n[j]
    if s < 2020:
        i += 1
    elif s > 2020:
        j -= 1
    else:
        print(f'P1: Found it! {n[i]} x {n[j]} = {n[i]*n[j]}')
        break

## part 2: find sum of 3 numbers == 2020. O(n^2)
found = False
i = 0
while i < len(n)-1:
    st = 2020 - n[i]
    if st < 0:
        break

    #Use alg from Part 1 for each subarray
    j, k = i + 1, len(n)-1
    while j != k:
        s = n[j] + n[k]
        if s < st:
            j += 1
        elif s > st:
            k -= 1
        else:
            print(f'P2: Found it! {n[i]} x {n[j]} x {n[k]} = {n[i]*n[j]*n[k]}')
            found = True
            break

    if found:
        break
    else:
        i += 1