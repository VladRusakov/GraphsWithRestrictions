from networkx import Graph
from graph_models.state_machine import StateMachine
from graph_models.networkx_based.layered_graph import LayeredGraph


def generate_layered_graph(graph: Graph, machine: StateMachine) -> LayeredGraph:
    layers = len(machine.elements)-1
    layered_graph = LayeredGraph(graph, layers)

    for u, v, key in graph.edges(keys=True):
        for level in range(layers):
            arc_type = graph.get_edge_data(u, v, key)['arc_type']
            operation_result = machine.apply(machine.elements[level], arc_type)
            if operation_result is not machine.forbidden:
                source = u + level * layered_graph.max_node
                dest = v + machine.elements.index(operation_result) * layered_graph.max_node
                layered_graph.add_edge(source, dest, origin_edge=key)

    return layered_graph
