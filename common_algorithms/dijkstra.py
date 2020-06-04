from math import inf
from heapq import heappush as insert, heappop as extract_minimum, nsmallest
from networkx import MultiDiGraph

from graph_models.networkx_based.layered_graph import LayeredGraph

COST = 'cost'
VISITED = 'visited'
WEIGHT = 'weight'
ARC = 'arc'
DEPTH = 'depth'


def calculate_dijkstra(source: int, layered_graph: LayeredGraph, ) -> MultiDiGraph:
    node_info = {node: {COST: inf, ARC: None, VISITED: False, DEPTH: inf} for node in layered_graph}
    node_info[source][COST] = 0
    node_info[source][DEPTH] = 0
    tree = MultiDiGraph()

    to_visit = []
    insert(to_visit, (0, source))
    images = {node: [] for node in layered_graph.origin_nodes}
    insert(images[layered_graph.origin_node_index(source)], ((0, 0), source))
    leafs = set()

    while len(to_visit) > 0:
        to_open = extract_minimum(to_visit)[1]
        if node_info[to_open][VISITED]:
            continue
        node_info[to_open][VISITED] = True

        for arc in layered_graph.out_edges(to_open, data=True):
            dest = arc[1]
            if not layered_graph.out_edges(dest):
                leafs.add(dest)
            new_cost = node_info[to_open][COST] + arc[2][WEIGHT]
            new_depth = node_info[to_open][DEPTH] + 1
            if node_info[dest][COST] > new_cost:
                node_info[dest][COST] = new_cost
                node_info[dest][ARC] = arc
                node_info[dest][DEPTH] = new_depth
                insert(to_visit, (new_cost, dest))
                insert(images[layered_graph.origin_node_index(dest)], ((new_cost, new_depth), dest))
                if not tree.has_edge(to_open, dest):  # TODO change on link to arc
                    tree.add_edge(to_open, dest)

    # node_info truncation - усечение дерева
    while leafs:
        leaf = leafs.pop()
        path_cost = node_info[leaf][COST]
        path_depth = node_info[leaf][DEPTH]
        if nsmallest(1, images[layered_graph.origin_node_index(leaf)]) != ((path_cost, path_depth), leaf):
            parent = node_info[leaf][ARC][0]
            tree.remove_edge(parent, leaf)
            if not tree.out_edges(parent):
                leafs.add(parent)

    return tree
