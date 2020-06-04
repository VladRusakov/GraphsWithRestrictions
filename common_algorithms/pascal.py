from typing import Dict, Iterable, List, Tuple
from math import inf
from networkx import MultiDiGraph

from graph_models.networkx_based.layered_graph import LayeredGraph


def pascal_for_layered(sources: List[int], layered_graph: LayeredGraph, max_path: int = inf) -> Tuple[dict, dict]:
    if max_path == 0:
        max_path = inf
    paths_on_layred = calculate_pascal(sources, layered_graph, max_path)
    paths_on_origin = {node: 0 for node in layered_graph.origin_nodes}
    for node, paths in paths_on_layred.items():
        if paths > 0:
            paths_on_origin[layered_graph.origin_node_index(node)] += paths
    return paths_on_origin, paths_on_layred


def calculate_pascal(sources: Iterable[int], graph: MultiDiGraph,  max_path: int = inf) -> Dict[int, int]:
    paths_count = {node: 0 for node in graph}
    to_update = {node_idx: 1 for node_idx in sources}
    path_len = 0

    while to_update and path_len <= max_path:
        to_update = pascal_iteration(graph, to_update, paths_count)
        path_len += 1

    return paths_count


def pascal_iteration(graph: MultiDiGraph, to_update: Dict[int, int], paths_count: Dict[int, int]) -> Dict[int, int]:
    new_to_update = {}

    for node, addition in to_update.items():
        paths_count[node] += addition

    for node in to_update:
        for arc in graph.out_edges(node):
            new_to_update[arc[1]] = new_to_update.get(arc[1], 0) + paths_count[node]

    return new_to_update
