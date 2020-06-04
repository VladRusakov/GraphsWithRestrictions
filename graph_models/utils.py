from typing import BinaryIO, List, Any, Dict

from networkx.classes import MultiDiGraph
from networkx.readwrite import parse_multiline_adjlist, generate_multiline_adjlist

from graph_models.networkx_based.layered_graph import LayeredGraph

encoding = 'utf-8'
comments = '#'
graph_section = f'{comments} graph section:'


def _find_str_index_in_list(string: str, str_list: List[str]) -> int or None:
    for index in range(len(str_list)):
        if string in str_list[index]:
            return index
    return None


def save_graph(graph: MultiDiGraph, path: str, header: str = '') -> None:
    with open(path, 'wb') as file:
        if header:
            file.write(header.encode(encoding))
        write_to_file(graph, file)


def read_graph(path: str, graph_type: type = MultiDiGraph):
    with open(path, 'rb') as file:
        lines = [line.decode(encoding) for line in file]
        delimiter = _find_str_index_in_list(graph_section, lines)
        attrs = parse_attrs(lines[:delimiter])
        attrs.insert(0, None)  # adding empty graph
        return parse_multiline_adjlist(iter(lines[delimiter:]), comments,
                                       create_using=graph_type(*attrs), nodetype=int)


def save_layered_graph(layered_graph: LayeredGraph, path: str) -> None:
    header = f'layers : {layered_graph.layers} \n' \
        f'origin_nodes : {layered_graph.origin_nodes} \n'
    save_graph(layered_graph, path, header)


def read_layered_graph(path: str) -> LayeredGraph:
    return read_graph(path, LayeredGraph)


def write_to_file(graph: MultiDiGraph, file: BinaryIO) -> None:
    file.write(graph_section.encode(encoding) + '\n')
    for multiline in generate_multiline_adjlist(graph):
        file.write((multiline + '\n').encode(encoding))


def parse_attrs(lines: List[str]) -> List[Any]:
    from ast import literal_eval
    attrs = []
    for line in lines:
        line = (line[:line.find(comments)]).strip()
        if line:
            field, data = line.split(':', maxsplit=1)
            attrs.append(literal_eval(data.strip()))
    return attrs
