from networkx import MultiDiGraph
from graph_models.networkx_based.layered_graph import LayeredGraph

arc_type = 'arc_type'
magnetic = 'm'
non_magnetic = 'n'


def non_decreasing_magnetism(graph: MultiDiGraph, k: int) -> LayeredGraph:
    layers = k + 1
    layered_graph = LayeredGraph(graph, layers)
    offset = layered_graph.max_node

    has_magnetic_outs = {node: magnetic in [arc[2][arc_type] for arc in graph.out_edges(node, data=True)]
                         for node in graph.nodes}

    for u, v, key in graph.edges(keys=True):
        edge_data = graph.get_edge_data(u, v, key)
        edge_type = edge_data[arc_type]
        if edge_type == magnetic:
            for level in range(k):
                source = u + level * offset
                dest = v + (level+1) * offset
                layered_graph.add_edge(source, dest, **edge_data)
            layered_graph.add_edge(u + k * offset, v + k * offset, **edge_data)

        elif edge_type == non_magnetic:
            for level in range(k):
                source = u + level * offset
                dest = v + level * offset
                layered_graph.add_edge(source, dest, **edge_data)
            if not has_magnetic_outs[u]:
                layered_graph.add_edge(u + k * offset, v + k * offset, **edge_data)
    return layered_graph
