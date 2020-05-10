class MainWindowModel:
    def __init__(self):
        self.graph = None
        self.layered_graph = None
        self.get_layered_method = None

    @property
    def graph(self):
        return self._graph

    @graph.setter
    def graph(self, graph):
        self._graph = graph

    @property
    def layered_graph(self):
        return self._layered_graph

    @layered_graph.setter
    def layered_graph(self, layered_graph):
        self._layered_graph = layered_graph
