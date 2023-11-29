import re
from collections import defaultdict


def procRulesToRE(rules):
    """Process rules to obtain a re for rule 0"""

    rules = dict(rules)  # copy
    recursionDepth = defaultdict(int)
    maxRecursion = 5
    noNumbers = lambda s: all(not c.isdigit() for c in s)

    while not noNumbers(rules[0]):
        depends = [int(i) for i in rules[0].split(" ") if i.isdigit()]
        for i in depends:
            if f" {i} " in rules[i]:
                recursionDepth[i] += 1

            replacement = f" ({rules[i]}) "
            if recursionDepth[i] >= maxRecursion:
                replacement = replacement.replace(f" {i} ", " ")

            rules[0] = rules[0].replace(f" {i} ", replacement)

    # Create re for rule 0
    r = re.compile(rules[0].replace(" ", "") + "$")
    return r


# Load rules
rerule = re.compile(r"(\d+): (.*)")
rules = {
    int(m.group(1)): " " + m.group(2).replace('"', "") + " "
    for m in [rerule.match(l) for l in open("./inputs/19", "r")]
    if m != None
}

# Part 1
r = procRulesToRE(rules)
matched = sum([1 for l in open("./inputs/19", "r") if r.match(l)])
print(f"P1: matched messages: {matched}")

# Part 2
# change rules 8 and 11
rules[8] = " 42 | 42 8 "
rules[11] = " 42 31 | 42 11 31 "

r = procRulesToRE(rules)
matched = sum([1 for l in open("./inputs/19", "r") if r.match(l)])
print(f"P2: matched messages: {matched}")
