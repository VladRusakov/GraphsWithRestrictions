from cayley_table import CayleyTable
from graph import Graph


class LayeredGraph(Graph):
    def __init__(self, layers: int, origin_nodes: int, origin_arcs: int):
        super.__init__()
        self.layers = layers
        self.origin_nodes = origin_nodes
        self.origin_arcs = origin_arcs

    def get_origin_node_index(self, node_index: int) -> int:
        return node_index % self.origin_nodes

    def get_origin_arc_id(self, arc_index: int) -> int:
        return arc_index % self.origin_arcs


def create_layered_graph(graph: Graph, table: CayleyTable) -> LayeredGraph:
    layered_graph = LayeredGraph()