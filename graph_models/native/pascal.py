from typing import Dict, Iterable
from math import inf
from graph_models.native.graph import Graph, OUT_ARCS


def calculate_pascal(graph: Graph, sources: Iterable[int], max_path: int = inf) -> Dict[int, int]:
    paths_count = {node: 0 for node in graph}
    to_update = {node_idx: 1 for node_idx in sources}
    path_len = 0

    while to_update and path_len <= max_path:
        to_update = pascal_iteration(graph, to_update, paths_count)
        path_len += 1

    return paths_count


def pascal_iteration(graph: Graph, to_update: Dict[int, int], paths_count: Dict[int, int]) -> Dict[int, int]:
    new_to_update = {}

    for node, addition in to_update.items():
        paths_count[node] += addition

    for node in to_update:
        for arc in graph[node][OUT_ARCS]:
            new_to_update[arc.dest] = new_to_update.get(arc.dest, 0) + paths_count[node]

    return new_to_update
