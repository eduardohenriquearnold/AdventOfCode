import re
import math

#Load specifications
specRE = re.compile('(.+): ((\d+)-(\d+)) or ((\d+)-(\d+))')
specs = {}

for line in open('./inputs/16', 'r'):
    if match := specRE.match(line):
        intervals = [int(n) for n in match.group(3,4,6,7)]
        specs[match.group(1)] = intervals

#P1: detect invalid nearby tickets
nearbyTickets = False
invalidSum = 0
validTickets = []
for line in open('./inputs/16', 'r'):
    if line.find('nearby tickets') > -1:
        nearbyTickets = True
        continue
    elif nearbyTickets:
        fields = [int(n) for n in  line.split(',')]
        validTicket = True
        for n in fields:
            anyValid = False
            for interval in specs.values():
                if (n >= interval[0] and n <= interval[1]) or (n >= interval[2] and n <= interval[3]):
                    anyValid = True
                    break
            if not anyValid:
                invalidSum += n
                validTicket = False
        if validTicket:
            validTickets.append(fields)
print(f'P1: invalid sum {invalidSum}')

#P2: identifying fields

#for each column, identify what field it CANNOT be (at least one row would be invalid)
nfields = len(validTickets[0])
cannot = [set() for _ in range(nfields)]
for ticket in validTickets:
    for col, n in enumerate(ticket):
        for field, interval in specs.items():
            if (n >= interval[0] and n <= interval[1]) or (n >= interval[2] and n <= interval[3]):
                continue
            else:
                cannot[col].add(field)

#now backtrack by identifying fields that have only a single possibility
mapping = {}
while len(mapping) < nfields:
    for i, c in enumerate(cannot):
        possibleFields = set(specs.keys()) - c
        if len(possibleFields) == 1:
            field = possibleFields.pop()
            mapping[field] = i
            for other in cannot:
                other.add(field)

#load my ticket
myTicket = False
for line in open('./inputs/16', 'r'):
    if line.find('your ticket') > -1:
        myTicket = True
        continue
    elif myTicket:
        myTicket = [int(n) for n in  line.split(',')]
        break

#compute product of keys starting with 'departure'
result = math.prod([myTicket[mapping[field]] for field in specs.keys() if 'departure' in field])
print(f'P2: The product of fields starting with "departure" is {result}')
