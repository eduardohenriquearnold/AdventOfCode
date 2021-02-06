def playGame(p1,p2):
    '''Play a whole game and returns which player won and the cards'''

    #make deep copy of the cards
    p1 = p1.copy()
    p2 = p2.copy()

    #Play game till end
    while len(p1)>0 and len(p2)>0:
        c1 = p1.pop(0)
        c2 = p2.pop(0)
        if c1>c2:
            p1 += [c1,c2]
        else:
            p2 += [c2,c1]

    if len(p1)>0:
        return 1, p1
    else:
        return 2, p2

def playGameRec(p1,p2):
    '''Play a game if the same set of cards hasn't hapened before, else victory of player 1'''

    #make copies
    p1 = p1.copy()
    p2 = p2.copy()

    #create list of hashes for game
    prevHashes = set()

    #Play game till end
    while len(p1)>0 and len(p2)>0:

        #Check if already played this game and add hash to collection if not
        chash = hash((tuple(p1), tuple(p2)))
        if chash  in prevHashes:
            return 1,list()
        prevHashes.add(chash)

        c1 = p1.pop(0)
        c2 = p2.pop(0)
 
        if c1<=len(p1) and c2<=len(p2):
            #play recursive game
            winner, _ = playGameRec(p1[:c1],p2[:c2])
        else:
            winner = 1 if c1>c2 else 2

        if winner == 1:
            p1 += [c1,c2]
        else:
            p2 += [c2,c1]

    if len(p1)>0:
        return 1, p1
    else:
        return 2, p2


#Load cards
p1 = []
p2 = []
for l in open('./inputs/22', 'r'):
    if 'Player 1' in l:
        cp = p1
    elif 'Player 2' in l:
        cp = p2
    else:
        try:
            cp.append(int(l.rstrip()))
        except ValueError:
            pass

#Play a game and compute score
_, cards = playGame(p1,p2)
s = sum([(i+1)*c for i,c in enumerate(cards[::-1])])
print(f'P1: final winner score {s}')

#Part 2 - play recursive combat
_, cards = playGameRec(p1,p2)
s = sum([(i+1)*c for i,c in enumerate(cards[::-1])])
print(f'P2: final winner score {s}')