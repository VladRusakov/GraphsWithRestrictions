from typing import Dict, Iterable, List
from math import inf
from networkx import MultiDiGraph

from graph_models.networkx_based.layered_graph import LayeredGraph


def pascal_for_layered(sources: List[int], graph: LayeredGraph, max_path_len: int = inf) -> Dict[int, int]:
    paths_on_layred = calculate_pascal(sources, graph, max_path_len)
    paths_on_origin = {node: 0 for node in graph.origin_nodes}
    for node, paths in paths_on_layred:
        if paths > 0:
            paths_on_origin[graph.origin_node_index(node)] += paths
    return paths_on_origin


def calculate_pascal(sources: Iterable[int], graph: MultiDiGraph,  max_path_len: int = inf) -> Dict[int, int]:
    paths_count = {node: 0 for node in graph}
    to_update = {node_idx: 1 for node_idx in sources}
    path_len = 0

    while to_update and path_len <= max_path_len:
        to_update = pascal_iteration(graph, to_update, paths_count)
        path_len += 1

    return paths_count


def pascal_iteration(graph: MultiDiGraph, to_update: Dict[int, int], paths_count: Dict[int, int]) -> Dict[int, int]:
    new_to_update = {}

    for node, addition in to_update.items():
        paths_count[node] += addition

    for node in to_update:
        for arc in graph.out_edges(node):
            new_to_update[arc.dest] = new_to_update.get(arc.dest, 0) + paths_count[node]

    return new_to_update
