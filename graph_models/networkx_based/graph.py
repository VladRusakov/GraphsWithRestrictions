from networkx import MultiDiGraph


class Graph(MultiDiGraph):

    def __init__(self, incoming_graph_data=None, **attr):
        super(MultiDiGraph).__init__(incoming_graph_data, **attr)

    def get_max_node(self):
        max_node = 0
        for node in self:
            max_node = node if node > max_node else max_node
        return max_node
