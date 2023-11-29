calories = []
current_calories = 0
with open("inputs/1.txt") as file:
    for line in file.readlines():
        line = line.strip()
        if line == "":
            calories.append(current_calories)
            current_calories = 0
        else:
            current_calories += int(line)

calories.sort()
print(calories[-1])
print(sum(calories[-3:]))
