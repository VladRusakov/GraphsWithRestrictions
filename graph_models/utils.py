from typing import BinaryIO, List, Any, Dict

from networkx.classes import MultiDiGraph
from networkx.readwrite import parse_multiline_adjlist, generate_multiline_adjlist

from graph_models.networkx_based.layered_graph import LayeredGraph

encoding = 'utf-8'
comments = '#'
graph_section = f'{comments} graph section:\n'


def save_graph(graph: MultiDiGraph, path: str, header: str = '') -> None:
    with open(path, 'wb') as file:
        if header:
            file.write(header, encoding)
        write_to_file(graph, file)


def read_graph(path: str, graph_type: type = MultiDiGraph):
    with open(path, 'rb') as file:
        lines = [line.decode(encoding) for line in file]
        delimiter = lines.index(graph_section)
        attrs = parse_attrs(lines[:delimiter])
        graph = parse_multiline_adjlist(lines[delimiter:], comments,
                                        create_using=MultiDiGraph, nodetype=int)
        return graph_type(graph, **attrs)


def save_layered_graph(layered_graph: LayeredGraph, path: str) -> None:
    header = f'layers : {layered_graph.layers} \n' \
        f'max_node : {layered_graph.max_node} \n' \
        f'origin_nodes : {layered_graph.origin_nodes} \n'
    save_graph(layered_graph, path, header)


def read_layered_graph(path: str) -> LayeredGraph:
    return read_graph(path, LayeredGraph)


def write_to_file(graph: MultiDiGraph, file: BinaryIO) -> None:
    file.write(graph_section)
    for multiline in generate_multiline_adjlist(graph):
        file.write(multiline.encode(encoding) + '\n')


def parse_attrs(lines: List[str]) -> Dict[str, Any]:
    attrs = {}
    for line in lines:
        line = (line[:line.find(comments)]).strip()
        if line:
            field, data = line.split(':', maxsplit=1)
            from ast import literal_eval
            attrs[field] = literal_eval(data)
    return attrs
