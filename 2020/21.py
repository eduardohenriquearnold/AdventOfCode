import numpy as np

#Load the recipes and alergens list
recipes = [] 
alergens = []
for l in open('./inputs/21','r'):
    brack = l.find('(')
    recipes.append(l[:brack-1].split(' '))
    alergens.append(l[brack+10:-2].split(', '))

#Part 1 - Create matrix showing the frequency that each ingredient appears in a recipe that has a given alergen
# M[alergens,ingredients]. M[i,j] = number of times that ingredient j appears in a recipe with alergen i
uingredients = {i:idx for idx, i in enumerate(set([i for ings in recipes for i in ings]))}
ualergens = {a:idx for idx, a in enumerate(set([a for als in alergens for a in als]))}
M = np.zeros((len(ualergens), len(uingredients)))
for ings,aler in zip(recipes, alergens):
    for ing in ings:
        for al in aler:
            M[ualergens[al], uingredients[ing]] += 1

#Check condition that specific ingredient cannot contain alergen, i.e. an ingredient cannot contain any alergen if the number of times it appears in a recipe with any alergen is smaller than the maximum number of times any ingredient appears with that allergen
maxCount = M.max(axis=1).reshape(-1,1)
cond = np.all(M<maxCount, axis=0)
invIngredients = dict(zip(uingredients.values(), uingredients.keys()))
alergenFree = [invIngredients[i] for i,v in enumerate(cond) if v]

#Count appearences
nAppearences = 0
for rec in recipes:
    for ing in rec:
        if ing in alergenFree:
            nAppearences += 1
print(f'P1: Alergen free ingredients appears {nAppearences} times')

#Part 2 - determine which ingredient has which alergen
mapping = {} #mapping from alergen index to ingredient index
Mp = M.copy() 
while len(mapping) < len(uingredients) - cond.sum():
    for i,row in enumerate(Mp):
        if -1 in row:
            continue
        maxV = row.max()
        if (row==maxV).sum() == 1:
            j = row.argmax()
            mapping[i] = j
            Mp[:,j] = 0
            Mp[i,j] = -1
#Sort alergen list
sAlergen = list(ualergens.keys())
sAlergen.sort()
sIngr = [invIngredients[mapping[ualergens[aler]]] for aler in sAlergen]
print(f'P2: dangerous list: {",".join(sIngr)}')