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
    capacity = float("inf") if start_path_arc in bounded_arcs else network.get_edge_data(*start_path_arc)[0]["capacity"]
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
        if paths_multiplicities[path] == 0:
            paths_capacities[path] = paths_simple_capacities[path]
            continue

        path_shared_capacity = residual_shared_capacity / paths_multiplicities[path]
        if path_shared_capacity >= paths_simple_capacities[path]:
            paths_capacities[path] = paths_simple_capacities[path]
            residual_shared_capacity -= paths_simple_capacities[path] * paths_multiplicities[path]
        else:
            paths_capacities[path] = path_shared_capacity
            break

    return sum(paths_capacities.values())


def calculate_multiplicity_reversed(end_path_arc, network: MultiDiGraph, source, bounded_arcs: set) -> int:
    multiplicity = 1 if end_path_arc in bounded_arcs else 0
    current_arc = end_path_arc
    while current_arc[0] is not source:
        arc_start = current_arc[0]
        current_arc = (list(network.predecessors(arc_start))[0], arc_start)
        multiplicity += 1 if current_arc in bounded_arcs else 0
    return multiplicity


def assign_path_capacity(network: MultiDiGraph, end_path_arc, source, bounded_arcs, residual_shared_capacity: float) \
        -> Tuple[float, float]:
    simple_capacity = float("inf")
    path_simple_arcs = set()
    path_bounded_arcs = set()
    if end_path_arc in bounded_arcs:
        path_bounded_arcs.add(end_path_arc)
    else:
        path_simple_arcs.add(end_path_arc)
        simple_capacity = network.get_edge_data(*end_path_arc)[0]["residual_capacity"]

    current_arc = end_path_arc
    while current_arc[0] is not source:
        arc_start = current_arc[0]
        current_arc = (list(network.predecessors(arc_start))[0], arc_start)
        if current_arc in bounded_arcs:
            path_bounded_arcs.add(current_arc)
            continue
        arc_capacity = network.get_edge_data(*current_arc)[0]["residual_capacity"]
        if arc_capacity == 0:
            return 0, residual_shared_capacity
        path_simple_arcs.add(current_arc)
        simple_capacity = simple_capacity if simple_capacity < arc_capacity else arc_capacity

    path_multiplicity = len(path_bounded_arcs)
    if not path_bounded_arcs:
        path_capacity = simple_capacity
    elif residual_shared_capacity / len(path_bounded_arcs) >= simple_capacity:
        path_capacity = simple_capacity
        residual_shared_capacity -= path_capacity * path_multiplicity
    else:
        path_capacity = residual_shared_capacity / len(path_bounded_arcs)
        residual_shared_capacity = 0

    for arc in path_simple_arcs:
        network.get_edge_data(*arc)[0]["residual_capacity"] -= path_capacity

    return path_capacity, residual_shared_capacity


def max_flow_in_tree_structured_network(network, source, sink, bounded_arcs, shared_capacity: float) -> float:
    paths_ends: List[Tuple] = list(network.in_edges(sink))
    paths_multiplicities = {path_end: calculate_multiplicity_reversed(path_end, network, source, bounded_arcs)
                            for path_end in paths_ends}

    for src, dst, attrs in network.edges(data=True):
        if (src, dst) not in bounded_arcs:
            attrs["residual_capacity"] = attrs["capacity"]

    residual_shared_capacity = shared_capacity

    paths_capacities = {path_end: 0 for path_end in paths_ends}
    paths_ordering = get_paths_order(paths_multiplicities, {path_end: 0 for path_end in paths_ends})
    for path_end in paths_ordering:
        paths_capacities[path_end], residual_shared_capacity = assign_path_capacity(network=network,
                                                                                    end_path_arc=path_end,
                                                                                    source=source,
                                                                                    bounded_arcs=bounded_arcs,
                                                                                    residual_shared_capacity=residual_shared_capacity
                                                                                    )

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

    print(max_flow_in_tree_structured_network(network=parallel_network,
                                              source=1,
                                              sink=4,
                                              bounded_arcs={(1, 2), (5, 6), (8, 9), (9, 10), (11, 4), (1, 4)},
                                              shared_capacity=20))
