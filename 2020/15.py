from collections import defaultdict

ipuzzle = [1,2,16,19,18,0]
rec = defaultdict(lambda: -1)
for i, n in enumerate(ipuzzle[:-1]):
    rec[n] = i + 1

last = ipuzzle[-1]
i = len(ipuzzle)
while (i < 30_000_000):
    if rec[last] == -1:
        rec[last] = i
        last = 0
    else:
        tmp = last
        last = i - rec[last]
        rec[tmp] = i 
    i += 1

    if i == 2020:
        print(f'Num {i} is {last}')
print(f'Num {i} is {last}')