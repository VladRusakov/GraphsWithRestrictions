import unittest
import networkx as nx
from table_generators.mixed_simple import generate_table_mixed_simple
from graph_generators.layered_from_table import generate_layered_graph


class TestCayleyTables(unittest.TestCase):

    def test_mixed_simple_create(self):
        table = generate_table_mixed_simple()
        self.assertEqual(table.apply('a', 'b'), 'b')
        self.assertEqual(table.apply('a', 'a'), 'a')
        self.assertEqual(table.apply('b', 'a'), 'a')
        self.assertEqual(table.apply('b', 'b'), 'z')
        self.assertEqual(table.apply('b', 'e'), 'b')
        self.assertEqual(table.apply('z', 'b'), 'z')

    def test_layered_simple(self):
        graph = nx.MultiDiGraph()
        graph.add_nodes_from(list(range(8)))
        graph.add_edge(0, 1, arc_type='a')
        graph.add_edge(0, 1, arc_type='b')
        graph.add_edge(0, 4, arc_type='b')
        graph.add_edge(4, 5, arc_type='a')
        graph.add_edge(3, 7, arc_type='a')
        graph.add_edge(6, 7, arc_type='a')

        graph.add_edge(4, 2, arc_type='b')
        graph.add_edge(1, 5, arc_type='b')
        graph.add_edge(1, 2, arc_type='b')
        graph.add_edge(2, 3, arc_type='b')
        graph.add_edge(5, 6, arc_type='b')
        table = generate_table_mixed_simple()

        layered_graph = generate_layered_graph(graph, table)
        pass

    def test_layered_very_simple(self):
        graph = nx.MultiDiGraph()
        graph.add_edge(0, 1, arc_type='a')
        graph.add_edge(0, 3, arc_type='b')
        graph.add_edge(3, 2, arc_type='b')
        graph.add_edge(1, 2, arc_type='a')
        table = generate_table_mixed_simple()

        layered_graph = generate_layered_graph(graph, table)

        from graph_models.utils import read_graph, read_layered_graph, save_layered_graph, save_graph
        save_graph(graph, '../data/mixed_simple_graph.txt')
        save_layered_graph(layered_graph, '../data/mixed_simple_layered_graph.txt')

        restored_graph = read_graph('../data/mixed_simple_graph.txt')
        restored_layered_graph = read_layered_graph('../data/mixed_simple_layered_graph.txt')
        self.assertEqual(graph.edges, restored_graph.edges)
        self.assertEqual(layered_graph.edges, restored_layered_graph.edges)


if __name__ == '__main__':
    unittest.main()
