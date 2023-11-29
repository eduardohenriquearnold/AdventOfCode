from functools import cmp_to_key


def load_packets(path):
    data = open(path, "r").read()
    pairs = data.split("\n\n")
    packet_pairs = [list(map(eval, pair.split("\n"))) for pair in pairs]
    return packet_pairs


def is_int(x):
    return isinstance(x, int)


def is_list(x):
    return isinstance(x, list)


def is_right_order(left_packet, right_packet):
    """Return 1 if right order, -1 otherwise"""

    for left, right in zip(left_packet, right_packet):
        if is_int(left) and is_int(right):
            if left < right:
                return 1
            elif left > right:
                return -1
        elif is_list(left) and is_list(right):
            if (res := is_right_order(left, right)) is None:  # fmt: skip
                continue
            else:
                return res
        elif is_int(left):
            if (res := is_right_order([left,],right,)) is None:  # fmt: skip
                continue
            else:
                return res
        elif is_int(right):
            if (res := is_right_order(left, [right,])) is None:  # fmt: skip
                continue
            else:
                return res

    # when run out of items
    if len(left_packet) < len(right_packet):
        return 1
    elif len(left_packet) > len(right_packet):
        return -1
    else:
        return None


def count_right_order(packet_pairs):
    count = 0

    for i, (left, right) in enumerate(packet_pairs):
        res = is_right_order(left, right)
        assert res is not None, "invalid result"
        count += i + 1 if res == 1 else 0
    return count


packet_pairs = load_packets("inputs/13.txt")
print(count_right_order(packet_pairs))

# additional divider packets
div0, div1 = [[2]], [[6]]
packet_pairs.append([div0, div1])

# get all packets - ignore pairs
packets = []
for pair in packet_pairs:
    packets.extend(pair)

packets.sort(key=cmp_to_key(is_right_order), reverse=True)
idx0 = packets.index(div0) + 1
idx1 = packets.index(div1) + 1
print(idx0 * idx1)
