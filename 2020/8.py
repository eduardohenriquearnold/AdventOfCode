# load commands and fill number of executed times to 0
cmds = [c.rstrip("\n") for c in open("./inputs/8", "r")]
ex = [0] * len(cmds)

# Part 1 - start execution
acc = 0
l = 0  # current line
executedLines = []
while ex[l] < 1:
    ex[l] += 1
    executedLines.append(l)
    cmd = cmds[l][:3]
    val = int(cmds[l][3:])
    if cmd == "acc":
        acc += val
    elif cmd == "jmp":
        l += val - 1
    l += 1
print(f"P1: The acc value before a line is executed a second time is: {acc}")

# Part 2
def run(changeLine=None):
    cmdsc = cmds.copy()
    if changeLine:
        cur = cmdsc[changeLine][:3]
        nxt = "nop" if cur == "jmp" else "jmp"
        cmdsc[changeLine] = cmdsc[changeLine].replace(cur, nxt)

    ex = [0] * len(cmds)
    acc = 0
    l = 0  # current line
    while ex[l] < 1:
        ex[l] += 1
        executedLines.append(l)
        cmd = cmdsc[l][:3]
        val = int(cmds[l][3:])
        if cmd == "acc":
            acc += val
        elif cmd == "jmp":
            l += val - 1
        l += 1

        if l == len(cmds):
            return True, acc
    return False, acc


# Brute force all alternatives of jmp/nop
for i, cmd in enumerate(cmds):
    if cmd[:3] in ["jmp", "nop"]:
        ended, acc = run(i)
        if ended:
            print(f"Acc after fixing problem: {acc}")
