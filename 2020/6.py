# Part 1
countOverall = 0
groupQ = set()
for personAnswer in open("./inputs/6", "r"):
    if personAnswer != "\n":
        for q in personAnswer.rstrip("\n"):
            groupQ.add(q)
    else:
        countOverall += len(groupQ)
        groupQ = set()
print(f"P1: Overall count: {countOverall}")

# Part 2
countOverall = 0
groupQ = dict()
groupSize = 0
for personAnswer in open("./inputs/6", "r"):
    if personAnswer != "\n":
        groupSize += 1
        for q in personAnswer.rstrip("\n"):
            groupQ[q] = groupQ.get(q, 0) + 1
    else:
        countOverall += sum([1 for (q, votes) in groupQ.items() if votes == groupSize])
        groupQ = dict()
        groupSize = 0
print(f"P2: Overall count: {countOverall}")
