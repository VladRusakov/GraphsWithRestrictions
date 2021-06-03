from flow_algorithms.Edmonds_Karp import EdmondsKarp
from graph_models.utils import read_layered_graph, read_graph

source_net = read_graph('../data/blocking_flow.txt')
layered_net = read_layered_graph('../data/blocking_flow_layered.txt')

max_flow = EdmondsKarp(layered_network=layered_net, network=source_net, s=0, t=31)

print(max_flow)