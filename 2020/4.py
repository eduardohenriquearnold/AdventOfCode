#Part 1
valid = 0
keys = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
curPassport = ''
for l in open('./inputs/4', 'r'):
    if len(l) > 1:
        curPassport = f'{curPassport} {l[:-1]}'
    else:
        s = sum([1 if curPassport.find(key)>=0 else 0 for key in keys])
        if s == len(keys):
            valid += 1
        curPassport = ''
print(f'P1: Valid Passports: {valid}')

#Part 2
import re
def validate(field, value):
    '''Determines if a given value is valid for the field'''

    #Numeric fields should be converted to integer first
    if field in ['byr','iyr','eyr']:
        try:
            value = int(value)
        except:
            return False

    if field == 'byr':
        return (value >= 1920 and value <= 2002)
    
    if field == 'iyr':
        return (value >= 2010 and value <= 2020)
    
    if field == 'eyr':
        return (value >= 2020 and value <= 2030)

    if field == 'hgt':
        try:
            h = int(value[:-2])
        except:
            return False
        if value[-2:] == 'cm':
            return (h >= 150 and h <= 193)
        elif value[-2:] == 'in':
            return (h >= 59 and h <= 76)
        else:
            return False

    if field == 'hcl':
        a = re.match('\#[0-9A-Fa-f]{6}', value)
        return a != None

    if field == 'ecl':
        return (value in 'amb blu brn gry grn hzl oth'.split())
    
    if field == 'pid':
        if len(value) != 9:
            return False
        try:
            value = int(value)
        except:
            return False
        return True

    return False

valid = 0
passport = {}
for l in open('./inputs/4', 'r'):
    if len(l) > 1:
        #gather passport data
        for pair in l.split():
            passport[pair[:3]] = pair[4:]
    else:
        #validate passport fields
        passport = {key:value for (key,value) in passport.items() if validate(key, value)}
        s = len(passport.items())
        #it's valid if all mandatory fields are available (and were validated)
        if s == len(keys):
            valid += 1
        passport = {}
print(f'P2: Valid Passports: {valid}')