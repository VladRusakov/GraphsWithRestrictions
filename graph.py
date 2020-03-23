from typing import Dict


class Graph:

    def __init__(self, nodes_count: int = 0):
        self._nodes = {}
        self._arc_index = 0
        self._node_index = nodes_count
        self._arcs_count = 0
        for node in range(self._node_index):
            self.nodes[node] = {'out_arcs': {}}

    def get_arcs(self):
        for node in self._nodes:
            for dest in self._nodes[node]['out_arcs']:
                for arc, info in self._nodes[node]['out_arcs'][dest].items():
                    yield (node, dest, arc, info)

    @property
    def nodes_count(self):
        return len(self._nodes)

    @property
    def arcs_count(self):
        return self._arcs_count

    def add_node(self):
        self.nodes[self._node_index] = {'out_arcs': {}}
        self._node_index += 1

    def add_arc(self, source: int, dest: int, info: Dict):
        new_arc = {self._arc_index: info}
        if self._nodes[source]['out_arcs'].get(dest) is not None:
            self._nodes[source]['out_arcs'][dest].update(new_arc)
        else:
            self._nodes[source]['out_arcs'][dest] = new_arc
        self._arc_index += 1
