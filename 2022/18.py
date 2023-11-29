from collections import deque

coordinate = tuple[int, int, int]


def load_input() -> set[coordinate]:
    """Loads list of coordinates from file into a set"""

    with open("inputs/18.txt", "r") as f:
        coords = set(tuple(int(v) for v in line.strip().split(",")) for line in f.readlines())
    return coords


def get_neighbours(coord: coordinate):
    yield from (
        tuple(sum(c) for c in zip(coord, delta))
        for delta in ((1, 0, 0), (0, 1, 0), (0, 0, 1), (-1, 0, 0), (0, -1, 0), (0, 0, -1))
    )


def compute_surface_area(coords: set[coordinate]) -> int:
    """Surface area is the number of neighbours that are empty (not in coords)"""
    return sum(
        1 for coord in coords for neigh_coord in get_neighbours(coord) if neigh_coord not in coords
    )


class BoundCheck:
    def __init__(self, coords: set[coordinate]):
        self.min = [min(c[i] - 1 for c in coords) for i in range(3)]
        self.max = [max(c[i] + 1 for c in coords) for i in range(3)]

    def within(self, coord):
        return all(self.min[i] <= coord[i] <= self.max[i] for i in range(3))


def find_connected_holes(coords: set[coordinate]) -> list[set[coordinate]]:
    """Connected component labelling (for holes)"""
    visited = set()
    components = []
    bounds = BoundCheck(coords)

    holes = (neigh for coord in coords for neigh in get_neighbours(coord) if neigh not in coords)
    for hole in holes:
        if hole in visited:
            continue
        visited.add(hole)
        component = set((hole,))
        queue = deque(get_neighbours(hole))
        while queue:
            coord = queue.pop()
            if coord in visited or coord in coords or not bounds.within(coord):
                continue
            component.add(coord)
            visited.add(coord)
            queue.extend(get_neighbours(coord))
        components.append(component)

    return components


def fill_holes(coords: set[coordinate]) -> None:
    components = find_connected_holes(coords=coords)
    components.sort(key=lambda l: len(l))
    # add all holes (except largest, i.e. out surface) to coords
    coords.update(*components[:-1])


def main():
    coords = load_input()
    area = compute_surface_area(coords=coords)
    print(area)

    fill_holes(coords)
    area_external = compute_surface_area(coords=coords)
    print(area_external)


if __name__ == "__main__":
    main()
