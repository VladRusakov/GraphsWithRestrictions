from cayley_table import CayleyTable


def generate_table_mixed_simple() -> CayleyTable:

    neutral = 'e'
    common = 'a'
    not_double = 'b'
    forbidden = 'z'
    elements = [neutral, common, not_double, forbidden]

    rules = {}
    for element in elements:
        rules[element] = {neutral: element}
    rules[neutral].update({element: element for element in elements})
    rules[common].update({common: common, not_double: not_double})
    rules[not_double].update({common: common, not_double: forbidden})

    return CayleyTable(elements, rules, forbidden)
