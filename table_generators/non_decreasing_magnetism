from graph_models.cayley_table import CayleyTable


def generate_table(k: int) -> CayleyTable:
    increase_symbol = 'a'
    forbidden = 'z'
    magnetic = 'm'
    neutral = 'n'
    elements = set(forbidden, magnetic, neutral)
    for level in range(k+1):
        elements.add(increase_symbol+str(level))
    rules = {}
    return CayleyTable(elements, rules, forbidden)
