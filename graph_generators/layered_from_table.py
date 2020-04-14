from graph_models.cayley_table import CayleyTable
from graph_models.networkx_based.graph import Graph
from graph_models.networkx_based.layered_graph import LayeredGraph


def generate_layered_graph(graph: Graph, table: CayleyTable) -> LayeredGraph:

    layered_graph = LayeredGraph(len(table.elements)-1, graph.nodes_count)

    for arc in graph.arcs:
        arc_type = arc.info['type']
        for level in range(table.elements):
            operation_result = table.apply(table.elements[level], arc_type)
            if operation_result is not table.forbidden:
                source = arc.source + level * graph.nodes_count
                dest = arc.dest + table.elements.find(operation_result) * graph.nodes_count
                info = {'origin_index': arc.index}.update(arc.info)
                layered_graph.add_edge(source, dest, info)

    return layered_graph
