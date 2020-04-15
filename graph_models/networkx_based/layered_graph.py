from typing import Collection, List
from networkx import MultiDiGraph
import networkx as nx
nx.shortest_path()

class LayeredGraph(MultiDiGraph):
    def __init__(self, graph: MultiDiGraph, layers: int):
        super().__init__(graph)
        self._layers = layers
        self._origin_nodes = list(graph.nodes)
        self._max_node = max(self.origin_nodes) + 1

    @property
    def layers(self):
        return self.layers

    @property
    def origin_nodes(self):
        return self._origin_nodes

    @property
    def max_node(self):
        return self._max_node

    def origin_node_index(self, node_index: int) -> int:
        if node_index not in self.nodes:
            raise ValueError('Node index should be integer and belong to graph')
        return node_index % self.max_node

    def get_node_layer(self, node_index: int) -> int:
        if node_index not in self.nodes:
            raise ValueError('Node index should be integer and belong to graph')
        return node_index // self.max_node

    def get_layer_nodes(self, layer: int) -> Collection[int]:
        if type(layer) != 'int' or layer < 0 or layer >= self.layers:
            raise ValueError('layer should be integer in range[0;layers)')
        layer_offset = layer * self.max_node
        for origin_node_index in self.origin_nodes:
            yield origin_node_index + layer_offset

    def get_connected_nodes(self, node_index: int) -> List[int]:
        if node_index not in self.nodes:
            raise ValueError('Node index should be integer and belong to graph')
        origin_node = node_index % self.max_node
        for layer in range(self.layers):
            yield origin_node + layer * self.max_node

    def get_origin_path(self, path_on_layered: Collection[int]) -> Collection[int]:
        pass


if __name__ == "__main__":
    import networkx as nx
    g = nx.complete_graph(3)
    lg = LayeredGraph(g, 2)
    print(lg.get_node_layer(12))
