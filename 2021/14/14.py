from typing import DefaultDict


def load(path):
    '''template-> string; dict: pair -> new_element'''
    with open(path, 'r') as f:
        template = f.readline().strip()
        rules = {}
        f.readline()
        for l in f.readlines():
            pair, new_element = l.strip().split(' -> ')
            rules[pair] = new_element
    return template, rules

def count_dict(template):
    count = DefaultDict(int)
    for i in range(len(template) - 1):
        pair = template[i:i+2]
        count[pair] += 1
    return count

def count_elements(t):
    count = DefaultDict(int)
    for c in t:
        count[c] += 1
    return count
 
def solve(t, rules, steps=1):
    count_pairs = count_dict(t)
    count_elem = count_elements(t)

    # perform steps
    for _ in range(steps):
        new_count_pairs = count_pairs.copy()
        for pair, count in count_pairs.items():
            if pair in rules:
                # apply rule
                new_count_pairs[pair] -= count

                # count new pairs
                pair_1 = ''.join((pair[0], rules[pair]))
                pair_2 = ''.join((rules[pair], pair[1]))
                new_count_pairs[pair_1] += count
                new_count_pairs[pair_2] += count

                # count new elements
                count_elem[rules[pair]] += count
            else:
                new_count_pairs[pair] = count
        count_pairs = new_count_pairs

    # count max and min elements
    ans = max(count_elem.values()) - min(count_elem.values())
    return ans


t, r = load('14/input.txt')
print(solve(t, r, 10))
print(solve(t, r, 40))

