from typing import Dict, Any
from math import inf
from heapq import heappush as insert, heappop as extract_minimum


COST = 'cost'
VISITED = 'visited'
WEIGHT = 'weight'
ARC = 'arc'


def calculate_dijkstra(graph: Graph, source: int) -> Dict[int, Dict[str, Any]]:
    result = {node: {COST: inf, ARC: None, VISITED: False} for node in graph}
    result[source][COST] = 0

    to_visit = []
    insert(to_visit, (0, source))

    while len(to_visit) > 0:
        to_open = extract_minimum(to_visit)[1]
        if result[to_open][VISITED]:
            continue
        result[to_open][VISITED] = True

        for arc in graph[to_open][OUT_ARCS]:
            new_cost = result[to_open][COST] + arc.info[WEIGHT]
            if result[arc.dest][COST] > new_cost:
                result[arc.dest][COST] = new_cost
                result[arc.dest][ARC] = arc.index
                insert(to_visit, (new_cost, arc.index))

    return result
