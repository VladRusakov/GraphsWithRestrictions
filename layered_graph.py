from graph import Graph


class LayeredGraph(Graph):
    def __init__(self, layers, origin_nodes, origin_arcs):
        super.__init__()
        # self.layers = layers - нужна ли вообще информация о слоях?
        self.origin_nodes = origin_nodes
        self.origin_arcs = origin_arcs

    def get_origin_node_index(self, node_index):
        return node_index % self.origin_nodes

    def get_origin_arc_id(self, arc_index):
        return arc_index % self.origin_arcs

def create_layered_graph(graph: Graph, table: CayleyTable) -> LayeredGraph:
    layered_graph = LayeredGraph()