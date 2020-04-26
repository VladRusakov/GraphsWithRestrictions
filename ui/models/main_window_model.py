class MainWindowModel:
    def __init__(self):
        self.graph = None
        self.layered_graph = None
        self.method = None
        self.get_layered_method = None

        self._observers = []

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

    def add_observer(self, new_observer):
        if new_observer not in self._observers:
            self._observers.append(new_observer)

    def remove_observer(self, removable_observer):
        self._observers.remove(removable_observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.model_is_changed()
