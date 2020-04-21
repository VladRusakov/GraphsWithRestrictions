from typing import Iterable, List
from networkx import Graph, MultiDiGraph


class LayeredGraph(MultiDiGraph):
    def __init__(self, graph: Graph = None, layers: int = 1, origin_nodes: List[int] = []):
        if graph is LayeredGraph:
            super().__init__(graph)
            graph = LayeredGraph(graph)
            self._layers = graph.layers
            self._origin_nodes = graph.origin_nodes.copy()
            self._max_node = graph.max_node
        else:
            if layers < 1:
                raise ValueError(f'layers count should be a positive integer, but got {layers}')
            super().__init__()
            self._layers = layers
            self._origin_nodes = origin_nodes if origin_nodes else list(graph.nodes)
            self._max_node = max(self.origin_nodes) + 1
            self._generate_layers()

    def _generate_layers(self):
        for layer in range(self.layers):
            self.add_nodes_from(node + layer * self.max_node for node in self.origin_nodes)

    @property
    def layers(self):
        return self._layers

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

    def get_layer_nodes(self, layer: int) -> Iterable[int]:
        if type(layer) != 'int' or layer < 0 or layer >= self.layers:
            raise ValueError('Layer should be integer in range[0;layers)')
        layer_offset = layer * self.max_node
        for origin_node_index in self.origin_nodes:
            yield origin_node_index + layer_offset

    def get_connected_nodes(self, node_index: int) -> List[int]:
        if node_index not in self.nodes:
            raise ValueError('Node index should be integer and belong to graph')
        origin_node = node_index % self.max_node
        for layer in range(self.layers):
            yield origin_node + layer * self.max_node

    def get_origin_path(self, path_on_layered: Iterable[int]) -> Iterable[int]:
        pass


if __name__ == "__main__":
    import networkx as nx
    g = nx.complete_graph(3)
    lg = LayeredGraph(g, 2)
    print(lg.nodes)
