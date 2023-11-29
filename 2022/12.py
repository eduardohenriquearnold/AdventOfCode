import numpy as np
from heapq import heappush, heappop


def load_heatmap(path) -> tuple[np.ndarray, tuple, tuple, tuple]:
    """Returns numpy form of heatmap ans starting/ending positions.
    Starting/ending positions have heights 0, 25 respectively.
    """
    content = open(path, "r").read()
    lines = content.count("\n") + 1
    content = content.replace("\n", "")
    h = np.array([ord(letter) - 97 for letter in content], copy=False).reshape((lines, -1))

    start = tuple(np.argwhere(h == -14)[0].tolist())
    end = tuple(np.argwhere(h == -28)[0].tolist())
    alt_starts = np.argwhere(h == 0)

    h[h == -14] = 0
    h[h == -28] = 25
    return h, start, end, alt_starts


def find_possible_movements(h: np.ndarray, cur_pos: tuple[int, int]):
    """From pos (vertical idx, horizontal idx), lists all possible movements"""
    possible = []

    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        pos = (cur_pos[0] + dy, cur_pos[1] + dx)

        if pos[0] >= 0 and pos[0] < h.shape[0] and pos[1] >= 0 and pos[1] < h.shape[1]:
            if h[pos[0], pos[1]] - h[cur_pos[0], cur_pos[1]] <= 1:
                possible.append(pos)

    return possible


def find_minimal_path(h: np.ndarray, start: tuple, end: tuple) -> int:
    visited = set()
    visit_next = []
    heappush(visit_next, (0, start))

    while len(visit_next) > 0:
        cost, pos = heappop(visit_next)
        if pos in visited:
            continue
        if pos == end:
            return cost
        visited.add(pos)

        for neighbour in find_possible_movements(h, pos):
            heappush(visit_next, (cost + 1, neighbour))

    return None


h, start, end, alt_starts = load_heatmap("inputs/12.txt")

# Part 1
min_path_length = find_minimal_path(h, start, end)
print(min_path_length)

# Part 2
for alt_start in alt_starts:
    alt_start = tuple(alt_start.tolist())
    length = find_minimal_path(h, alt_start, end)
    if length is not None:
        min_path_length = min(min_path_length, length)
print(min_path_length)
