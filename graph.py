class Graph:
    def __new_node(cls):
        return node++

    class Arc:
        pass

    def __init__(self, nodes_count:int = 0):
        self.nodes = {}
        for node in range(nodes_count):
            self.nodes[node] = None

    def add_node(self):

    def add_arc(self, source, destination):
        self.nodes[source][] = None

    def add_arc(self, name: str or int) -> None:
        pass


class LayeredGraph(Graph):
    def __init__(self, layers):
        super.__init__()
        self.layers = layers

    def get_origin_node(self, node):
        return self.nodes[node]  # что-то такое
