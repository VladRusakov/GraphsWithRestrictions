from networkx import MultiDiGraph
from queue import Queue


def check_source_and_sink(network: MultiDiGraph, source, sink) -> None:
    if source not in network:
        raise ValueError('source node does not belong to the network')
    if sink not in network:
        raise ValueError('sink node does not belong to the network')
    if source == sink:
        raise ValueError('source and sink is the same node')


def is_parallel(network: MultiDiGraph, source, sink) -> bool:
    """
    Checks whether given network is parallel or not.
    :param network: flow network
    :param source: source node
    :param sink: sink node
    :return:
    """
    check_source_and_sink(network=network, source=source, sink=sink)

    if len(list(network.successors(source))) != len(list(network.predecessors(sink))):
        return False

    source_sink = {source, sink}
    nodes_to_visit = set(network.nodes).difference(source_sink)

    parallel_branches = set(network.successors(source)).difference(source_sink)
    for node in parallel_branches:
        while node != sink:
            node_successors = list(network.successors(node))
            if len(node_successors) != 1:
                return False
            if len(list(network.predecessors(node))) != 1:
                return False
            try:
                nodes_to_visit.remove(node)
            except KeyError:
                return False
            node = node_successors[0]

    if len(nodes_to_visit) > 0:
        return False

    return True


def is_tree_structured(network: MultiDiGraph, source, sink) -> bool:
    check_source_and_sink(network=network, source=source, sink=sink)
    if len(list(network.predecessors(source))) > 0:
        return False
    if len(list(network.successors(sink))) > 0:
        return False

    source_sink = {source, sink}
    nodes_to_process = Queue()
    for node in network.successors(source):
        nodes_to_process.put(node)

    nodes_to_visit = set(network.nodes).difference(source_sink)

    while not nodes_to_process.empty():
        node = nodes_to_process.get()

        if len(list(network.predecessors(node))) != 1:
            return False

        try:
            nodes_to_visit.remove(node)
        except KeyError:
            return False

        for node in network.successors(node):
            if node is not sink:
                nodes_to_process.put(node)

    if len(nodes_to_visit) != 0:
        return False

    return True


if __name__ == '__main__':
    parallel_network = MultiDiGraph([
        # (0, 1),
        (1, 2), (2, 3), (3, 4),
        (1, 5), (5, 6), (6, 7), (7, 4),
        (1, 8), (8, 9), (9, 10), (10, 11), (11, 4),
        (1, 12), (12, 4),
    ])
    print(is_parallel(parallel_network, 1, 4))
    print(is_tree_structured(parallel_network, 1, 4))
