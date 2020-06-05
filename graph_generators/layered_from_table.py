from networkx import Graph
from graph_models.cayley_table import CayleyTable
from graph_models.networkx_based.layered_graph import LayeredGraph


def generate_layered_graph(graph: Graph, table: CayleyTable) -> LayeredGraph:
    layers = len(table.elements)-1
    layered_graph = LayeredGraph(graph, layers)

    for u, v, key in graph.edges(keys=True):
        for level in range(layers):
            edge_data = graph.get_edge_data(u, v, key)
            arc_type = edge_data['arc_type']
            operation_result = table.apply(table.elements[level], arc_type)
            if operation_result is not table.forbidden:
                source = u + level * layered_graph.max_node
                dest = v + table.elements.index(operation_result) * layered_graph.max_node
                layered_graph.add_edge(source, dest, origin_edge=key, **edge_data)

    return layered_graph
