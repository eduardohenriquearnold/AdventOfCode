from typing import DefaultDict
import heapq


def load(path):
    risk = DefaultDict(lambda: float('inf'))
    with open(path, 'r') as f:
        for i, l in enumerate(f.readlines()):
            for j, val in enumerate(l.strip()):
                risk[(i,j)] = float(val)
    H, W = i + 1, j + 1
    return (H, W), risk

def neighbours(pos):
    neigh = []
    for di, dj in ((-1,0), (1,0), (0,-1), (0,1)):
        neigh.append((pos[0]+di, pos[1]+dj))
    return neigh

def dijk(size, risk):
    H, W = size
    dist = DefaultDict(lambda: float('inf'))
    unvisited = [(i, j) for i in range(H) for j in range(W)]
    dist[(0,0)] = 0

    while(len(unvisited) > 0):
        cur_pos = unvisited.pop(0)

        # recompute distance to neighbours
        for npos in neighbours(cur_pos):
            dist[npos] = min(dist[npos], dist[cur_pos]+risk[npos])

        # sort unvisited according to distance
        unvisited.sort(key=lambda x: dist[x])

    return dist

def dijk_pq(size, risk):
    dist = DefaultDict(lambda: float('inf'))
    dist[(0,0)] = 0

    unvisited = [(0, (0,0))]
    while(len(unvisited) > 0):
        cur_distance, cur_pos = heapq.heappop(unvisited)

        # recompute distance to neighbours
        for npos in neighbours(cur_pos):
            distance = cur_distance + risk[npos]

            # if distance through current node smaller, update neighbour distance and add neighbour to unvisited queue
            if distance < dist[npos]:
                dist[npos] = distance
                heapq.heappush(unvisited, (distance, npos))

    return dist

def extend_map(size, r):
    H, W = size

    #extended risk
    er = DefaultDict(lambda: float('inf'))

    for it in range(5):
        for jt in range(5):
            for pos, val in r.items():
                new_pos = (pos[0]+H*it, pos[1]+W*jt)
                new_val = val + it + jt
                new_val = (new_val % 10) + 1 if new_val > 9 else new_val
                er[new_pos] = new_val

    return (5*H, 5*W), er 

size, r = load('15/input.txt')

#part1
cr = dijk_pq(size, r.copy())
H, W = size
print(cr[(H-1, W-1)])

#part2
esize, er = extend_map(size, r)
cr = dijk_pq(esize, er)
H, W = esize
print(cr[(H-1, W-1)])