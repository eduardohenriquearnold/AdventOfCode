from typing import DefaultDict


def load(path):
    with open(path, 'r') as f:
        lines = [x.strip() for x in f.readlines()]
    return lines
    
def error_score(lines):
    dic = {'}':'{',
           ')':'(',
           ']':'[',
           '>':'<'}
    pts = {'}':1197,
           ')':3,
           ']':57,
           '>':25137}

    score = 0
    incomplete_lines = []
    for l in lines:
        stack = []
        error = False
        for x in l:
            if x in dic.values():
                stack.append(x)
            elif x in dic.keys():
                p = stack.pop(-1)
                if p != dic[x]:
                    score += pts[x]
                    error = True
                    break
        if not error:
            incomplete_lines.append(l)
    return score, incomplete_lines

def complete_lines(lines):
    dic = {'}':'{',
           ')':'(',
           ']':'[',
           '>':'<'}
    dic_inv = {v:k for k,v in dic.items()}
    pts = {')':1,
           ']':2,
           '}':3,
           '>':4}
        
    scores = []
    for l in lines:
        stack = []
        # creates stack
        for x in l:
            if x in dic.values():
                stack.append(x)
            elif x in dic.keys():
                stack.pop(-1)

        # scores remaining stack
        l_score = 0
        for x in stack[::-1]:
            l_score *= 5
            l_score += pts[dic_inv[x]]
        scores.append(l_score)

    # return median score
    scores.sort()
    median_score = scores[len(scores)//2]
    return median_score

l = load('10/input.txt')
r1, incomplete = error_score(l)
r2 = complete_lines(incomplete)
print(r1)
print(r2)
        
