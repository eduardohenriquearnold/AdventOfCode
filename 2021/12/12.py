from typing import DefaultDict

def load(path):
    dic = DefaultDict(list)
    with open(path, 'r') as f:
        for l in f.readlines():
            u, v = l.strip().split('-')

            if v != 'start':
                dic[u].append(v)
            if u != 'start':
                dic[v].append(u)
    return dic

def valid_route_1(r):
    '''check if a route is valid: a single visit to small caves are allowed'''

    # count words
    count = DefaultDict(int)
    for w in r:
        count[w] += 1

    # check for repeated small caves
    for w, c in count.items():
        # ignore big caves
        if w.isupper():
            continue

        if c > 1:
            return False

    return True

def valid_route_2(r):
    '''check if a route is valid: a single small cave can be visited twice, the rest small caves can only be visited once'''

    # count words
    count = DefaultDict(int)
    for w in r:
        count[w] += 1

    # check for repeated small caves
    greater_two = 0
    for w, c in count.items():
        # ignore big caves
        if w.isupper():
            continue

        if c == 2:
            greater_two += 1
        elif c > 2:
            return False

    return greater_two <= 1

def trace(dic, valid_route_f):
    routes = [['start',], ]

    added_items = 1
    while added_items > 0:
        added_items = 0
        new_routes = []

        # add next step for all possible routes
        for r in routes:
            # if route has reached the end, skip
            if r[-1] == 'end':
                new_routes.append(r)
                continue

            # otherwise, create other routes with all possible next stops
            for next_stop in dic[r[-1]]:
                r_new = r.copy()
                r_new.append(next_stop)
                new_routes.append(r_new)
                added_items += 1

        # get rid of routes that visit small cave more than twice
        new_routes = list(filter(valid_route_f, new_routes))
        routes = new_routes
    return routes
        

dic = load('12/input.txt')
# part1
routes = trace(dic, valid_route_1)
print(len(routes))
# part2
routes = trace(dic, valid_route_2)
print(len(routes))
