from typing import DefaultDict


def load(path):
    ins, outs = [], []
    with open(path, 'r') as f:
        for l in f.readlines():
            i, o = l.split('|')
            ins.append(i.strip().split(' '))
            outs.append(o.strip().split(' '))
    return ins, outs
    
def part1(ins, outs):
    '''counts the number of outs with 2,3,4 and 7 'wires' correpsonding to numbers 1,4,7 and 8, respectively'''

    counts = DefaultDict(int)
    for out in outs:
        for word in out:
            counts[len(word)] += 1

    return sum([counts[i] for i in (2,3,4,7)])

def sorted_string(s):
    return ''.join(sorted(s))

def part2(ins, outs):
    s = 0
    for i, o in zip(ins, outs):
        dic = {}
        i = sorted(i, key=lambda s: len(s))

        dic[sorted_string(i[0])] = 1
        dic[sorted_string(i[1])] = 7
        dic[sorted_string(i[2])] = 4
        dic[sorted_string(i[9])] = 8

        # solve remaining
        # 5 digits
        sel = i[3:6]
        for x in sel:
            if len(set(x).intersection(set(i[1]))) == 3:
                dic[sorted_string(x)] = 3
                sel.remove(x)
                break
        for x in sel:
            if len(set(x).intersection(set(i[2]))) == 3:
                dic[sorted_string(x)] = 5
                five_repr = sorted_string(x)
                sel.remove(x)
                break
        dic[sorted_string(sel[0])] = 2

        # 6 digits
        sel = i[6:10]
        for x in sel:
            if len(set(x).intersection(set(i[2]))) == 4:
                dic[sorted_string(x)] = 9
                sel.remove(x)
                break
        for x in sel:
            if len(set(x).intersection(set(five_repr))) == 5:
                dic[sorted_string(x)] = 6
                sel.remove(x)
                break
        dic[sorted_string(sel[0])] = 0

        # compute output number and sum
        s += 1000*dic[sorted_string(o[0])] + 100*dic[sorted_string(o[1])] + 10*dic[sorted_string(o[2])] + dic[sorted_string(o[3])]
    return s


ins, outs = load('8/input.txt')
r1 = part1(ins, outs)
r2 = part2(ins, outs)
print(f'P1: {r1}')
print(f'P2: {r2}')

