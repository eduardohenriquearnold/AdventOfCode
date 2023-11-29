import re

coordinate = tuple[int, int]


def load_input(path) -> dict[coordinate, coordinate]:
    exp = re.compile(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)\s?")

    sensor_beacon = dict()
    for line in open(path, "r").readlines():
        if result := exp.match(line):
            sx, sy, bx, by = tuple(map(int, result.groups()))
            sensor_beacon[(sx, sy)] = (bx, by)
        else:
            raise RuntimeError(f"Unexpected input: {line}")

    return sensor_beacon


def distance(s: coordinate, b: coordinate) -> int:
    """Manhattan distance"""
    return abs(s[0] - b[0]) + abs(s[1] - b[1])


def row_exclusion(sensor_beacon: dict, row: int) -> set[coordinate]:
    """Returns positions within row that CANNOT have a beacon"""
    no_beacon = set()
    for sensor, beacon in sensor_beacon.items():
        dist = distance(sensor, beacon)
        diff = abs(row - sensor[1])
        for i in range(dist - diff + 1):
            no_beacon.add((sensor[0] - i, row))
            no_beacon.add((sensor[0] + i, row))

    return no_beacon


def perimeter(sensor, beacon):
    dist = distance(sensor, beacon)
    for i in range(dist + 1):
        yield (sensor[0] + dist + 1 - i, sensor[1] + i)
        yield (sensor[0] + dist + 1 - i, sensor[1] - i)
        yield (sensor[0] - dist - 1 + i, sensor[1] - i)
        yield (sensor[0] - dist - 1 + i, sensor[1] + i)


def find_stress_beacon(sensor_beacon: dict, max_coord: int) -> coordinate:
    """Find stress beacon by looking into every cell of the external perimeter of each sensor.
    It is the stress beacon if it's not within the range of any other sensor"""

    sensor_beacon_distance = {s: (b, distance(s, b)) for s, b in sensor_beacon.items()}

    for sensor, beacon in sensor_beacon.items():
        for pos in perimeter(sensor, beacon):
            if pos[0] < 0 or pos[1] < 0 or pos[0] > max_coord or pos[1] > max_coord:
                continue

            # check if current pos is outside all other sensors' perimiters
            outside_all_perimeters = True
            for other_sensor, (_, sb_dist) in sensor_beacon_distance.items():
                if other_sensor == sensor:
                    continue

                if distance(other_sensor, pos) <= sb_dist:
                    outside_all_perimeters = False
                    break

            # if so, then this must be the stress beacon
            if outside_all_perimeters:
                return pos


sensor_beacon = load_input("inputs/15.txt")

# P1
no_beacon_pos = row_exclusion(sensor_beacon=sensor_beacon, row=2000000) - set(sensor_beacon.values())
print(len(no_beacon_pos))

# P2
beacon = find_stress_beacon(sensor_beacon, 4000000)
print(beacon)
tuning_frequency = 4000000 * beacon[0] + beacon[1]
print(tuning_frequency)
