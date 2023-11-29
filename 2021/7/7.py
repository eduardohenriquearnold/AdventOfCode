from statistics import median, mean

with open('7/input.txt', 'r') as f:
    crabs = list(map(int, f.readline().strip().split(',')))

# Part 1
# find the position c that minimises the fuel consumption F, where F = sum(abs(crab[i] - c))
# the optimal c is the median of crab positions
c = int(median(crabs))
F = sum([abs(pos-c) for pos in crabs])
print(f'Part1: {F}')

# Part 2
# we now have F(c) = sum(0.5 * abs(pos-c) * (1 + abs(pos-c))) for pos in crabs
# differentiating F(c) w.r.t. c and equating it to zero yields c + 1/(2*n) * sum(sign(pos-c)) = mean(crabs)
# this equation holds for when median(crabs) = mean(crabs) => c=mean(crabs)
c = int(mean(crabs))
F = int(sum([0.5*(1+abs(pos-c))*abs(pos-c) for pos in crabs]))
print(f'Part2: {F}')