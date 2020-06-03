from queue import Queue

from networkx import MultiDiGraph

from graph_models.networkx_based.layered_graph import LayeredGraph

not_processed = 'Н'
viewed = 'П'
processed = 'О'
mark = 'mark'
depth = 'depth'


def breadth_first(start: int, graph: LayeredGraph):
    node_info = {node: {mark: not_processed, depth: 0} for node in graph.nodes}
    image = {origin_node: [] for origin_node in graph.origin_nodes}
    tree = MultiDiGraph()
    to_process = Queue()
    leafs = Queue()
    node_info[start] = viewed
    to_process.put(start)

    while not to_process.empty():
        to_open = to_process.get()
        image[graph.origin_node_index(to_open)].append(to_open)

        arcs = graph.out_edges(to_open)
        if arcs:
            for arc in arcs:
                if node_info[arc.dest][mark] == not_processed:
                    node_info[arc.dest][mark] = viewed
                    node_info[arc.dest][depth] = node_info[to_open][depth] + 1
                    to_process.put(arc.dest)
                    tree.add_edge(to_open, arc.dest)
        else:
            leafs.put(to_open)
        node_info[to_open] = processed

    while not leafs.empty():
        leaf = leafs.get()
        images = image[graph.origin_node_index(leaf)]
        if images[0] != leaf:
            leaf_source = tree.in_edges(leaf)[0].source
            tree.remove_node(leaf)
            if not tree.out_edges(leaf_source):
                leafs.put(leaf_source)

    return tree
