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
    capacity = 0 if start_path_arc not in bounded_arcs else start_path_arc.capacity
    current_arc = start_path_arc
    while current_arc[1] is not sink:
        arc_end = current_arc[1]
        current_arc = (arc_end, list(network.successors(arc_end))[0])
        capacity = capacity if capacity < arc_capacity else arc_capacity
    return capacity


def max_flow_in_parallel_network(network: MultiDiGraph, source, sink, bounded_arcs: Set[Tuple], shared_capacity: float) -> float:
    paths_starts: List[Tuple] = list(network.out_edges(source))
    paths_multiplicities = {path: calculate_multiplicity(path, network, sink, bounded_arcs) for path in paths_starts}
    paths_simple_capacities = {path: calculate_simple_capacity(path, network, sink, bounded_arcs) for path in paths_starts}
    residual_shared_capacity = shared_capacity
    paths_capacities = {path: 0 for path in paths_starts}
    paths_order = [...]
    for path in paths_order:
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
        (1, 2), (2, 3), (3, 4),
        (1, 5), (5, 6), (6, 7), (7, 4),
        (1, 8), (8, 9), (9, 10), (10, 11), (11, 4),
        (1, 12), (12, 4),
        (1, 4),
    ])
    print(max_flow_in_parallel_network(network=parallel_network,
                                       source=1,
                                       sink=4,
                                       bounded_arcs={(1, 2), (5, 6), (8, 9), (9, 10), (11, 4), (1, 4)},
                                       shared_capacity=20)
          )
