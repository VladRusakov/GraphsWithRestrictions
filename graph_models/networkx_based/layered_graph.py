from typing import Collection
from networkx import MultiDiGraph


class LayeredGraph(MultiDiGraph):
    def __init__(self, graph: MultiDiGraph, layers: int):
        super().__init__(graph)
        self._layers = layers
        self._origin_nodes = list(graph.nodes)
        self._max_node = max(self.origin_nodes)

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
        return node_index % self.max_node

    def get_node_layer(self, node_index: int) -> int:
        return node_index // self.max_node

    def get_layer_nodes(self, layer: int) -> Collection[int]:
        for node_index in range(self.origin_nodes * layer, self.origin_nodes * (layer+1)):
            yield node_index

    def get_origin_path(self, path_on_layered: Collection[int]) -> Collection[int]:
        pass
        #return (arc[] for )


if __name__ == "__main__":
    import networkx as nx
    g = nx.complete_graph(3)
    lg = LayeredGraph(g, 2)
    print(lg.origin_nodes)
