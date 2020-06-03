from collections import Callable

from networkx import MultiDiGraph

from graph_models.networkx_based.layered_graph import LayeredGraph
from ui.utils.model import Observable, update_observers


class MainWindowModel(Observable):
    def __init__(self):
        super().__init__()
        self.graph: MultiDiGraph = None
        self.layered_graph: LayeredGraph = None
        self.get_layered_method: Callable = None

    @property
    def graph(self):
        return self._graph

    @graph.setter
    @update_observers
    def graph(self, graph) -> MultiDiGraph:
        self._graph = graph

    @property
    def layered_graph(self) -> LayeredGraph:
        return self._layered_graph

    @layered_graph.setter
    @update_observers
    def layered_graph(self, layered_graph):
        self._layered_graph = layered_graph
        self.notify_observers()
