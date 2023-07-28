from typing import Set, Tuple, List

from networkx import MultiDiGraph


def calculate_multiplicity(start_path_arc, network: MultiDiGraph, sink, bounded_arcs: set) -> int:
    multiplicity = 1 if start_path_arc in bounded_arcs else 0
    current_arc = start_path_arc
    while current_arc[1] is not sink:
        arc_end = current_arc[1]
        current_arc = (arc_end, list(network.successors(arc_end))[0])
        multiplicity += 1 if current_arc in bounded_arcs else 0
    return multiplicity


def calculate_simple_capacity(start_path_arc, network: MultiDiGraph, sink, bounded_arcs: set) -> float:
    capacity = 0 if start_path_arc in bounded_arcs else network.get_edge_data(*start_path_arc)[0]["capacity"]
    current_arc = start_path_arc
    while current_arc[1] is not sink:
        arc_end = current_arc[1]
        current_arc = (arc_end, list(network.successors(arc_end))[0])
        if current_arc not in bounded_arcs:
            arc_capacity = network.get_edge_data(*current_arc)[0]["capacity"]
            capacity = capacity if capacity < arc_capacity else arc_capacity
    return capacity


def get_paths_order(paths_multiplicities: dict, paths_simple_capacities: dict) -> List[str]:
    paths_characteristics = [
        {
            "path_start": path,
            "multiplicity": paths_multiplicities[path],
            "capacity": paths_simple_capacities[path]
        }
        for path in paths_multiplicities]
    paths_order = sorted(paths_characteristics, key=lambda k: (k["multiplicity"], -k["capacity"]))
    return [path["path_start"] for path in paths_order]


def max_flow_in_parallel_network(network: MultiDiGraph, source, sink, bounded_arcs: Set[Tuple], shared_capacity: float) -> float:
    paths_starts: List[Tuple] = list(network.out_edges(source))
    paths_multiplicities = {path: calculate_multiplicity(path, network, sink, bounded_arcs) for path in paths_starts}
    paths_simple_capacities = {path: calculate_simple_capacity(path, network, sink, bounded_arcs) for path in paths_starts}
    residual_shared_capacity = shared_capacity
    paths_capacities = {path: 0 for path in paths_starts}
    paths_ordering = get_paths_order(paths_multiplicities, paths_simple_capacities)
    for path in paths_ordering:
        if residual_shared_capacity == 0:
            break
        if paths_multiplicities[path] == 0:
            paths_capacities[path] = paths_simple_capacities[path]
            continue

        path_shared_capacity = residual_shared_capacity / paths_multiplicities[path]
        if path_shared_capacity >= paths_simple_capacities[path]:
            paths_capacities[path] = paths_simple_capacities[path]
            residual_shared_capacity -= paths_simple_capacities[path] * paths_multiplicities[path]
        else:
            paths_capacities[path] = path_shared_capacity
            residual_shared_capacity = 0

    return sum(paths_capacities.values())


if __name__ == '__main__':
    parallel_network = MultiDiGraph([
        # (0, 1),
        (1, 2), (2, 3, dict(capacity=3)), (3, 4, dict(capacity=3.5)),
        (1, 5, dict(capacity=2)), (5, 6), (6, 7, dict(capacity=3)), (7, 4, dict(capacity=2)),
        (1, 8, dict(capacity=4)), (8, 9), (9, 10), (10, 11, dict(capacity=3)), (11, 4, dict(capacity=2)),
        (1, 12, dict(capacity=1)), (12, 4, dict(capacity=1)),
        (1, 4),
    ])
    print(max_flow_in_parallel_network(network=parallel_network,
                                       source=1,
                                       sink=4,
                                       bounded_arcs={(1, 2), (5, 6), (8, 9), (9, 10), (11, 4), (1, 4)},
                                       shared_capacity=20)
          )
