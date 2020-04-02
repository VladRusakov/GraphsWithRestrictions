from cayley_table import CayleyTable


def generate_table_mixed(max_in_row: int) -> CayleyTable:

    if not isinstance(max_in_row, int):
        raise TypeError('max_in_row should be integer')
    if max_in_row < 1 and max_in_row:
        raise ValueError('max_in_row should be greater than 0')

    simple = 'e'
    increase = 'b'
    forbidden = 'z'
    monoid = set(increase + str(index) for index in range(1, barrier_height + 1))
    monoid.add(forbidden, barrier, neutral)

    rules = {}
    for element in monoid:
        rules[element] = {neutral: element}
    rules[neutral].update({element: element for element in monoid})

    for index in range(1, barrier_height):
        rules[increase + str(index)].update({increase + str(1): increase + str(index + 1),
                                             barrier: forbidden})
    rules[increase + str(barrier_height)].update({increase + str(1): increase + barrier_height,
                                                  barrier: neutral})
    return CayleyTable(monoid, rules, forbidden)
