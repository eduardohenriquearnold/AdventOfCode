with open('3/input.txt', 'r') as f:
    numbers = [line.rstrip() for line in f.readlines()]
n = len(numbers)
m = len(numbers[0])

def binlist2num(l):
    return int("".join(l), 2)

# part 1
def count_ones(numbers):
    assert len(numbers) > 0
    counts = [0,] * len(numbers[0])
    for number in numbers:
        for i, b in enumerate(number):
            counts[i] += int(b)
    return counts

counts = count_ones(numbers)

gamma, eps = [], []
for c in counts:
    if c >= n//2:
        gamma.append('1')
        eps.append('0')
    else:
        gamma.append('0')
        eps.append('1')
gamma = binlist2num(gamma)
eps = binlist2num(eps)
print(f'part 1: {gamma*eps}')

# part 2
def counter(numbers, counts, type):
    assert type in ('oxy', 'co2')

    nums = numbers.copy()

    bit = 0
    while len(nums) > 1:
        counts = count_ones(nums)

        keep = []
        for num in nums:
            most_common = '1' if counts[bit] >= len(nums) - counts[bit] else '0'
            least_common = '0' if counts[bit] >= len(nums) - counts[bit] else '1'

            if type == 'oxy' and num[bit] == most_common:
                keep.append(num) 
            
            if type =='co2' and num[bit] == least_common:
                keep.append(num)

        nums = keep.copy()
        bit += 1

    return nums[0]

oxy_rating = binlist2num(counter(numbers, counts, 'oxy'))
co2_rating = binlist2num(counter(numbers, counts, 'co2'))
life_rating = oxy_rating * co2_rating
print(f'part2: {life_rating}')





