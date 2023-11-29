import re
from heapq import heappush, heappop
from itertools import combinations


def load_input(path) -> tuple[dict[str, int], dict[str, list[str]]]:
    flows = dict()
    tunnels = dict()

    exp = re.compile(r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.+)\s?")
    for line in open(path, "r").readlines():
        if match := exp.match(line):
            valve, flow, connections = match.groups()
            flows[valve] = int(flow)
            tunnels[valve] = connections.split(", ")
        else:
            raise RuntimeError(f"Unexpected input: {line}")

    return flows, tunnels


def eval_solution(solution: dict[str, int], flows: dict[str, int]) -> int:
    """Evaluate a solution by computing the total flow after time.
    Solution has form of dict, mapping the valve to the timestamp when it opens"""

    return sum((flows[valve] * (TOTAL_TIME - open_time) for valve, open_time in solution.items()))


def shortest_path(start: str, end: str, tunnels: dict[str, list[str]]) -> int:
    """Returns the shortest path length between start and end nodes. Return none if no path can be found"""
    visited = set()
    visit_next = list()
    heappush(visit_next, (0, start))

    while len(visit_next) > 0:
        steps, current = heappop(visit_next)
        if current in visited:
            continue
        elif current == end:
            return steps
        else:
            visited.add(current)
            for node in tunnels[current]:
                heappush(visit_next, (steps + 1, node))

    return None


def shortest_path_dict(tunnels: dict[str, list[str]]) -> dict:
    """Create dict with shortest path between any two nodes"""

    sp = dict()
    for node1 in tunnels.keys():
        for node2 in tunnels.keys():
            sp[(node1, node2)] = shortest_path(start=node1, end=node2, tunnels=tunnels)
            sp[(node2, node1)] = shortest_path(start=node2, end=node1, tunnels=tunnels)
    return sp


def partial_solutions(current_valves, times, all_valves, shortest_paths):
    yielded = False
    for v in all_valves - set(current_valves):
        step = shortest_paths[(current_valves[-1], v)]
        if step is None:
            continue
        new_time = times[-1] + step + 1
        if new_time >= TOTAL_TIME:
            continue
        yielded = True
        yield from partial_solutions(current_valves + (v,), times + (new_time,), all_valves, shortest_paths)

    if not yielded:
        yield {valve: time for valve, time in zip(current_valves, times)}


def get_max_pressure(valves, shortest_paths, flows):
    max_pressure = 0
    for solution in partial_solutions(("AA",), (0,), set(valves), shortest_paths):
        max_pressure = max(max_pressure, eval_solution(solution, flows))
    return max_pressure


def find_optimal_solution(flows: dict[str, int], tunnels: dict[str, list[str]], elephant=False) -> int:
    """Iterate over possible solutions, keep the highest score"""

    shortest_paths = shortest_path_dict(tunnels=tunnels)
    valves = tuple(v for v, p in flows.items() if p > 0)  # ignores 0 pressure valves, including AA

    num_valves_me = len(valves) // 2 if elephant else len(valves)
    highest_pressure = 0
    for valves_me in combinations(valves, num_valves_me):
        valves_elephant = set(valves) - set(valves_me)

        highest_pressure = max(
            get_max_pressure(valves_me, shortest_paths, flows)
            + get_max_pressure(valves_elephant, shortest_paths, flows),
            highest_pressure,
        )

    return highest_pressure


flows, tunnels = load_input("inputs/16.txt")

# P1
TOTAL_TIME = 30
max_pressure = find_optimal_solution(flows, tunnels)
print(max_pressure)

# P2
TOTAL_TIME = 26
max_pressure = find_optimal_solution(flows, tunnels, elephant=True)
print(max_pressure)
