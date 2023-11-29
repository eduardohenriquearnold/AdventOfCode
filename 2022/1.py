calories = []
current_calories = 0
for line in open("inputs/1.txt").readlines():
    line = line.strip()
    if line == "":
        calories.append(current_calories)
        current_calories = 0
    else:
        current_calories += int(line)

calories.sort()
print(calories[-1])
print(sum(calories[-3:]))
