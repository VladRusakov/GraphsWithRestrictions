from typing import BinaryIO, Iterable

from networkx.classes import MultiDiGraph
from networkx.readwrite import parse_multiline_adjlist, generate_multiline_adjlist

encoding='utf-8'
comments='#'

def save_graph(graph: MultiDiGraph, path: str, header: str = '') -> None:
    with open(path, 'wb') as file:
        write_to_file(graph, file)


def read_graph(path: str):
    with open(path, 'rb') as file:

    return MultiDiGraph(read_multiline_adjlist(path, nodetype=int, edgetype=int))


def save_layered_graph(layeredgraph, path: str) -> None:
    pass


def read_layered_graph(path: str):
    pass


def write_to_file(graph: MultiDiGraph, file: BinaryIO):
    file.write(f'{comments} adjacency lists of graph:')
    for multiline in generate_multiline_adjlist(graph):
        file.write(multiline.encode(encoding) + '\n')
