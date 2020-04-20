from typing import Generator, Iterable
from graph_models.native.graph import Graph


class LayeredGraph(Graph):
    def __init__(self, layers: int, origin_nodes: int):
        super().__init__(layers*origin_nodes)
        self.layers = layers
        self.origin_nodes = origin_nodes

    def origin_node_index(self, node_index: int) -> int:
        return node_index % self.origin_nodes

    def get_node_layer(self, node_index: int) -> int:
        return node_index // self.origin_nodes

    def get_layer_nodes(self, layer: int) -> Generator[int]:
        for node_index in range(self.origin_nodes * layer, self.origin_nodes * (layer+1)):
            yield node_index

    def get_origin_path(self, path_on_layered: Iterable[int]) -> Iterable[int]:
        pass
