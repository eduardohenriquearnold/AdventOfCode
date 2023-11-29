def hex2bin(hs):
    '''convert hex string to binary string'''
    dic = {'0':'0000',
           '1':'0001',
           '2':'0010',
           '3':'0011',
           '4':'0100',
           '5':'0101',
           '6':'0110',
           '7':'0111',
           '8':'1000',
           '9':'1001',
           'A':'1010',
           'B':'1011',
           'C':'1100',
           'D':'1101',
           'E':'1110',
           'F':'1111',
          }

    bin_str = (dic[v] for v in hs.strip())
    return ''.join(bin_str)

def decode(s, max_packets=None):
    packets = []

    while(len(s) > 0 and '1' in s):
        # if we're given a max number of packets, return when those are obtained (also return remaining string)
        if max_packets is not None:
            if len(packets) >= max_packets:
                return packets, s

        # decode
        version = int(s[:3], 2)
        type = int(s[3:6], 2)

        if type == 4:
            literal = []
            current = 6
            while True:
                literal.append(s[current+1 : current+5])
                if s[current] == '0':
                    break
                current += 5
            literal = ''.join(literal)
            literal = int(literal, 2)
            packets.append({'version':version, 'type':type, 'literal':literal})
            s = s[current+5:]
        else:
            length_type = s[6]
            subpackets = []

            if length_type == '0':
                length_bits = int(s[7:7+14+1], 2)
                subpackets, _ = decode(s[22 : 22+length_bits])
                s = s[22+length_bits:]
            else:
                num_subpackets = int(s[7 : 7+11], 2)
                subpackets, s = decode(s[18:], max_packets=num_subpackets) 

            packets.append({'version':version, 'type':type, 'subpackets':subpackets})

    return packets, s

def sum_versions(packets):
    p = packets.copy()
    s = 0
    while len(p) > 0:
        pp = p.pop()
        s += pp['version']
        if 'subpackets' in pp:
            p.extend(pp['subpackets'])
    return s

def eval(p):
    # if literal, the result is its number
    if 'literal' in p:
        return p['literal']

    # else, we need to evaluate subpackets
    vals = tuple(eval(sp) for sp in p['subpackets'])

    # then, aggregate results depending on type
    t = p['type']
    if t == 0:
        return sum(vals)
    elif t == 1:
        r = 1
        for v in vals:
            r *= v
        return r
    elif t == 2:
        return min(vals)
    elif t == 3:
        return max(vals)
    elif t == 5:
        return 1 if vals[0] > vals[1] else 0
    elif t == 6:
        return 1 if vals[0] < vals[1] else 0
    elif t == 7:
        return 1 if vals[0] == vals[1] else 0
    else:
        raise ValueError('Invalid type number')

with open('16/input.txt') as f:
    msg = f.readline().strip()
packets, _ = decode(hex2bin(msg))
# part1
print(sum_versions(packets))
# part 2
print(eval(packets[0]))
