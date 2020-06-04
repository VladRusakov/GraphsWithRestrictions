from queue import Queue
from typing import Tuple

from networkx import MultiDiGraph

from graph_models.networkx_based.layered_graph import LayeredGraph

not_processed = 'Н'
viewed = 'П'
processed = 'О'
mark = 'mark'
depth = 'depth'


def breadth_first(source: int, layered_graph: LayeredGraph) -> Tuple[MultiDiGraph, MultiDiGraph]:
    node_info = {node: {mark: not_processed, depth: 0} for node in layered_graph.nodes}
    image = {origin_node: [] for origin_node in layered_graph.origin_nodes}
    tree = MultiDiGraph()
    to_process = Queue()
    leafs = Queue()
    node_info[source][mark] = viewed
    to_process.put(source)

    while not to_process.empty():
        to_open = to_process.get()
        image[layered_graph.origin_node_index(to_open)].append(to_open)

        arcs = layered_graph.out_edges(to_open)
        if arcs:
            for arc in arcs:
                dest = arc[1]
                if node_info[dest][mark] == not_processed:
                    node_info[dest][mark] = viewed
                    node_info[dest][depth] = node_info[to_open][depth] + 1
                    to_process.put(dest)
                    tree.add_edge(to_open, dest)
        else:
            leafs.put(to_open)
        node_info[to_open][mark] = processed

    not_truncated_tree = MultiDiGraph(tree)
    while not leafs.empty():
        leaf = leafs.get()
        images = image[layered_graph.origin_node_index(leaf)]
        if images[0] != leaf:
            leaf_source = list(tree.in_edges(leaf))[0][0]
            tree.remove_node(leaf)
            if not tree.out_edges(leaf_source):
                leafs.put(leaf_source)

    return tree, not_truncated_tree
