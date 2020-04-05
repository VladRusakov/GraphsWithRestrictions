from collections import Dict, Collection

from graph import Graph


def calculate_paths_count(graph: Graph, sources: Collection[int], max_path_len: int = None) -> Dict[int, int]:

    class node_info:
        def __init__(self, paths, addition):
            self.paths = paths
            self.addition = addition
            self.new_addition

    paths_count = {node: node_info(0, 0) for node in graph}
    for node in sources:
        paths_count[node].node_info.addition = 1

    R = len(sources)
    R2 = 0

    while R != R2:
        for node in paths_count:
            node.node_info.paths += node.node_info.addition
            node.node_info.new_addition = 0

        R2 = 0
        for arc in graph.get_arcs():
            paths_count[arc.dest].node_info.new_addition += paths_count[arc.source].addition
            R2 += paths_count[arc.source].addition

    return {}
