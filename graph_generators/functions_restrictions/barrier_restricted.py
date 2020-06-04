from networkx import MultiDiGraph
from ...graph_models.networkx_based.layered_graph import LayeredGraph


def barrier_restricted(graph: MultiDiGraph, k: int) -> LayeredGraph:
    layers = k + 1
    layered_graph = LayeredGraph(graph, layers)
    offset = layered_graph.max_node

    for u, v, key in graph.edges(keys=True):
        arc_type = graph.get_edge_data(u, v, key)['arc_type']

        if arc_type == 'e':
            for level in range(layers):
                source = u + level * offset
                dest = v + level * offset
                layered_graph.add_edge(source, dest, origin_edge=key)

        elif arc_type == 'a':
            for level in range(k):
                source = u + level * offset
                dest = v + (level+1) * offset
                layered_graph.add_edge(source, dest, origin_edge=key)
            layered_graph.add_edge(u + k * offset, v + k * offset, origin_edge=key)

        elif arc_type == 'b':
            layered_graph.add_edge(u + k * offset, v + k * offset, origin_edge=key)

    return layered_graph
