from typing import List

from networkx import MultiDiGraph

from graph_models.networkx_based.layered_graph import LayeredGraph

not_processed = 'Н'
viewed = 'П'
processed = 'О'
mark = 'mark'


def find_cycle_nodes(source: int, graph: MultiDiGraph) -> set[int]:
    cycle_nodes = set()
    node_info = {node: not_processed for node in graph.nodes}
    to_process = [source]

    while to_process:
        node = to_process[-1]
        if node_info[node] == processed:
            to_process.pop()
            continue
        has_append = False
        for arc in graph.out_edges(node):
            if node_info[arc.dest] == viewed:
                cycle_nodes.add(arc.dest)
            elif node_info[arc.dest] == not_processed:
                to_process.append(arc.dest)
                has_append = True
        if has_append:
            continue
        to_process.pop()
        node_info[node] = processed
    return cycle_nodes


def has_cycle_on_origin(source: int, graph: LayeredGraph) -> bool:
    node_info = {node: not_processed for node in graph.origin_nodes}
    to_process = [source]
    while to_process:
        node = to_process[-1]
        if node_info[graph.origin_node_index(node)] == processed:
            to_process.pop()
            continue
        has_append = False
        for arc in graph.out_edges(node):
            if node_info[graph.origin_node_index(arc.dest)] == viewed:
                return True
            elif node_info[graph.origin_node_index(arc.dest)] == not_processed:
                to_process.append(arc.dest)
                has_append = True
        if has_append:
            continue
        to_process.pop()
        node_info[graph.origin_node_index(node)] = processed
    return False


def depth_first_has_cycle(source: int, origin_graph: MultiDiGraph, layered_graph: LayeredGraph) -> bool:
    cycle_nodes = find_cycle_nodes(source, origin_graph)
    for node in cycle_nodes:
        if has_cycle_on_origin(node, layered_graph):
            return True
    return False
