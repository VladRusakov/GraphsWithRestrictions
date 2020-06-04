from typing import Set

from networkx import MultiDiGraph

from graph_models.networkx_based.layered_graph import LayeredGraph

not_processed = 'Н'
viewed = 'П'
processed = 'О'
mark = 'mark'


def find_cycle_nodes(source: int, graph: MultiDiGraph) -> Set[int]:
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
            dest = arc[1]
            if node_info[dest] == viewed:
                cycle_nodes.add(dest)
            elif node_info[dest] == not_processed:
                to_process.append(dest)
                has_append = True
        if has_append:
            node_info[node] = viewed
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
            dest = arc[1]
            dest_origin = graph.origin_node_index(dest)
            if node_info[dest_origin] == viewed:
                return True
            elif node_info[dest_origin] == not_processed:
                to_process.append(dest)
                has_append = True
        if has_append:
            node_info[dest_origin] = viewed
            continue
        to_process.pop()
        node_info[graph.origin_node_index(node)] = processed
    return False


def depth_first_has_cycle(source: int, graph: MultiDiGraph, layered_graph: LayeredGraph) -> bool:
    cycle_nodes = find_cycle_nodes(source, graph)
    for node in cycle_nodes:
        if has_cycle_on_origin(node, layered_graph):
            return True, cycle_nodes
    return False, cycle_nodes
