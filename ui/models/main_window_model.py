from ui.utils.model import Observable, update_observers


class MainWindowModel(Observable):
    def __init__(self):
        super().__init__()
        self.graph = None
        self.layered_graph = None
        self.get_layered_method = None

    @property
    def graph(self):
        return self._graph

    @graph.setter
    @update_observers
    def graph(self, graph):
        self._graph = graph

    @property
    def layered_graph(self):
        return self._layered_graph

    @layered_graph.setter
    @update_observers
    def layered_graph(self, layered_graph):
        self._layered_graph = layered_graph
        self.notify_observers()
