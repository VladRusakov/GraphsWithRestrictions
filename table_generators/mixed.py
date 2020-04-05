from cayley_table import CayleyTable


def generate_table_mixed(max_in_row: int) -> CayleyTable:

    if not isinstance(max_in_row, int):
        raise TypeError('max_in_row should be integer')
    if max_in_row < 1 and max_in_row:
        raise ValueError('max_in_row should be greater than 0')

    simple = 'e'
    increase = 'b'
    forbidden = 'z'
    elements = set(increase + str(index) for index in range(1, barrier_height + 1))
    elements.add(forbidden, barrier, neutral)

    rules = {}
    for element in elements:
        rules[element] = {neutral: element}
    rules[neutral].update({element: element for element in elements})

    for index in range(1, barrier_height):
        rules[increase + str(index)].update({increase + str(1): increase + str(index + 1),
                                             barrier: forbidden})
    rules[increase + str(barrier_height)].update({increase + str(1): increase + barrier_height,
                                                  barrier: neutral})
    return CayleyTable(elements, rules, forbidden)
