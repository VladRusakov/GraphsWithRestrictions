from typing import Dict, Any, Generator

OUT_ARCS = 'out_arcs'


class Graph:

    class Arc:
        def __init__(self, index: int, source: int, dest: int, info: Dict[str, Any] = {}):
            self.index = index
            self.source = source
            self.dest = dest
            self.info = info

    def __init__(self, nodes_count: int = 0):
        self._nodes = {}
        self._arc_index = 0
        self._node_index = nodes_count
        self._arcs_count = 0
        for node in range(self._node_index):
            self.nodes[node] = {OUT_ARCS: []}

    def __getitem__(self, node_index):
        return self._nodes[node_index]

    def __iter__(self):
        return (node for node in self._nodes)

    @property
    def arcs(self) -> Generator[Arc]:
        for node in self._nodes:
            for arc in self._nodes[node][OUT_ARCS]:
                yield arc

    @property
    def nodes_count(self):
        return len(self._nodes)

    @property
    def arcs_count(self):
        return self._arcs_count

    def add_node(self):
        self.nodes[self._node_index] = {OUT_ARCS: []}
        self._node_index += 1

    def add_edge(self, source: int, dest: int, info: Dict):
        new_arc = self.Arc(self._arc_index, source, dest, info)
        self._nodes[source][OUT_ARCS].append(new_arc)
        self._arc_index += 1
