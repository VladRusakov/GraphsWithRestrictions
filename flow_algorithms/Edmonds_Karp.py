from queue import Queue
from typing import List, Dict, Any, Tuple

from math import inf
from networkx import Graph, MultiDiGraph

from graph_models.networkx_based.layered_graph import LayeredGraph


class Labels:
    not_processed = 'Н'
    processed = 'О'
    viewed = 'П'


class NodeAttrs:
    in_arc = 'in_arc'
    label = 'label'


class ArcAttrs:
    arc_type = 'arc_type'
    direction = 'direction'
    flow = 'flow'
    res_capacity = 'residual'


class ArcPart:
    source = 0
    dest = 1
    key = 2
    attrs = 3


class Directions:
    reverse = 'reverse'
    straight = 'straight'


def unite_sinks(network: LayeredGraph, t: int):
    """
    Adds new sink into network for all sinks in layered network which are referenced with one origin sink t
    :param network: layered network built by origin flow network and a reachability restriction
    :param t: origin flow network sink
    :return:
    """
    united_sink = network.max_node * network.layers  # it's supposed that max_node is number of any layer nodes
    network.add_node(united_sink)  # nodes are enumerated from 0 and the new sink will have number of nodes count
    for sink in list(network.get_connected_nodes(t)):
        network.add_edge(sink, united_sink, c=inf)


def cut_dead_ends(network: LayeredGraph, s: int, t: int):
    # is it neccesary to cut redundant nodes for an experiment?
    pass


def build_flow_network(network: LayeredGraph) -> LayeredGraph:
    """
    Creates reverse arcs for every arc in layered graph to execute Edmonds-Karp algorithm
    :param network: layered flow network
    :return: a new performed layered network with reverse arcs
    """
    flow_network = LayeredGraph(network)
    for source, dest, key, attrs in network.edges(data=True, keys=True):
        flow_network[source][dest][key].update({
            ArcAttrs.flow: 0,
            ArcAttrs.direction: Directions.straight
        })
        flow_network.add_edge(dest, source, **{
            ArcAttrs.flow: 0,
            ArcAttrs.arc_type: attrs[ArcAttrs.arc_type],
            ArcAttrs.direction: Directions.reverse,
        })
    return flow_network


def search_path(flow_network: LayeredGraph, source_network: Graph, s: int, t: int) -> List[int] or None:
    """
    Looks for valid augmenting path
    :param flow_network: auxiliary network built by source flow network and a reachability restriction
    :param source_network: flow network with arc capacitites
    :param s: source flow network node
    :param t: sink node
    :return: valid path for augmenting or None if no one found
    """

    nodes_visit = {node: {NodeAttrs.label: Labels.not_processed, NodeAttrs.in_arc: None}
                   for node in flow_network.nodes}
    nodes_visit[s][NodeAttrs.label] = Labels.viewed
    to_process = Queue()
    to_process.put(s)

    sink_nodes = list(flow_network.get_connected_nodes(t))

    while not to_process.empty():
        to_open = to_process.get()

        if to_open in sink_nodes:
            return build_path(to_open, nodes_visit)

        for arc in flow_network.out_edges(to_open, keys=True, data=True):
            origin_source = flow_network.origin_node_index(arc[ArcPart.source])
            origin_dest = flow_network.origin_node_index(arc[ArcPart.dest])
            if arc[ArcPart.attrs][ArcAttrs.direction] == Directions.reverse or \
                    source_network[origin_source][origin_dest][arc[ArcPart.attrs][ArcAttrs.arc_type]][ArcAttrs.res_capacity] > 0:
                dest = arc[ArcPart.dest]
                if nodes_visit[dest][NodeAttrs.label] == Labels.not_processed:
                    nodes_visit[dest][NodeAttrs.label] = Labels.viewed
                    nodes_visit[dest][NodeAttrs.in_arc] = arc
                    to_process.put(dest)

        nodes_visit[to_open][NodeAttrs.label] = Labels.processed

    return None  # no one valid augmenting path has been found


def build_path(last_node: int, nodes_visit: Dict[int, Dict[str, Any]]) -> List:
    """
    Creates path from info about nodes and theirs input arcs found by network traverse
    :param last_node: last node in path. Should be the sink of flow network
    :param nodes_visit: information about network traverse
    :return:
    """
    path = []
    while True:
        in_arc = nodes_visit[last_node][NodeAttrs.in_arc]
        if in_arc is not None:
            path.append(in_arc)
            last_node = in_arc[ArcPart.source]
        else:
            break
    path.reverse()
    return path


def augment(path, flow_network: LayeredGraph, source_network: MultiDiGraph) -> None:
    min_capacity = inf
    for arc in path:
        if arc[ArcPart.attrs][ArcAttrs.direction] == Directions.reverse:
            continue
        origin_source = flow_network.origin_node_index(arc[ArcPart.source])
        origin_dest = flow_network.origin_node_index(arc[ArcPart.dest])
        arc_type = arc[ArcPart.attrs][ArcAttrs.arc_type]
        res_capacity = source_network[origin_source][origin_dest][arc_type][ArcAttrs.res_capacity]
        if res_capacity < min_capacity:
            min_capacity = res_capacity

    if min_capacity == inf:
        raise ValueError('path has infinite capacity')

    for arc in path:
        layered_source = arc[ArcPart.source]
        layered_dest = arc[ArcPart.dest]
        origin_source = flow_network.origin_node_index(layered_source)
        origin_dest = flow_network.origin_node_index(layered_dest)
        arc_type = arc[ArcPart.attrs][ArcAttrs.arc_type]
        if arc[ArcPart.attrs][ArcAttrs.direction] == Directions.straight:
            source_network[origin_source][origin_dest][arc_type][ArcAttrs.res_capacity] -= min_capacity
            # flow_network[layered_source][layered_dest][arc_type][ArcAttrs.flow] += min_capacity
        else:
            source_network[origin_dest][origin_source][arc_type][ArcAttrs.res_capacity] += min_capacity
            # flow_network[layered_source][layered_dest][arc_type][ArcAttrs.flow] -= min_capacity


def gather_in_flows(node: int, flow_network: LayeredGraph) -> int:
    """
    Sums all input flows into sink from all levels of layered graph
    :param node: sink node of any level
    :param flow_network: layered network with flow values assigned for arcs
    :return: amount of node input flow
    """
    connected_nodes = flow_network.get_connected_nodes(node)
    flow_sum = 0
    for node in connected_nodes:
        input_arcs = flow_network.in_edges(node, keys=True, data=True)
        flow_sum += sum(arc[ArcPart.attrs][ArcAttrs.flow] for arc in input_arcs if arc[ArcPart.attrs][ArcAttrs.direction] == Directions.straight)
    return flow_sum


def EdmondsKarp(layered_network: LayeredGraph, network: Graph, s: int, t: int, capacity_label: str = 'c') -> int:
    # unite_sinks(network=layered_network, t=t)
    # united_sink = layered_network.max_node * layered_network.layers
    # cut_dead_ends(layered_network, s=s, t=t)

    source_net = MultiDiGraph()
    for src, dst, key, data in network.edges(data=True, keys=True):
        new_key = data[ArcAttrs.arc_type]
        source_net.add_edge(src, dst, key=new_key, **data)
        source_net[src][dst][new_key][ArcAttrs.res_capacity] = data[capacity_label]

    flow_network = build_flow_network(layered_network)  # create auxiliary network with reversed arcs

    while True:
        path = search_path(flow_network=flow_network, source_network=source_net, s=s, t=t)
        if path:
            augment(path, flow_network=flow_network, source_network=source_net)
        else:
            return gather_in_flows(node=t, flow_network=flow_network)
