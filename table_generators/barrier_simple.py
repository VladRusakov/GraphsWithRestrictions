from graph_models.cayley_table import CayleyTable


def generate_table_barrier_simple(barrier_height: int) -> CayleyTable:
    """
    создание таблицы Кэли для барьерной достижимости уровня barrier_height
    :param barrier_height: уровень барьерной достижимости
    :return: таблица Кэли
    """
    if not isinstance(barrier_height, int):
        raise TypeError('barrier_height should be integer')
    if barrier_height < 1 and barrier_height:
        raise ValueError('barrier_height should be greater than 0')

    forbidden = 'z'
    barrier = 'b'
    neutral = 'e'
    increase = 'a'
    elements = set(increase + str(index) for index in range(1, barrier_height+1))
    elements.add(forbidden, barrier, neutral)

    rules = {}
    for element in elements:
        rules[element] = {neutral: element}
    rules[neutral].update({element: element for element in elements})

    for index in range(1, barrier_height):
        rules[increase + str(index)].update({increase+str(1): increase + str(index+1),
                                             barrier: forbidden})
    rules[increase+str(barrier_height)].update({increase+str(1): increase+str(barrier_height),
                                                barrier: neutral})
    return CayleyTable(list(elements), rules, forbidden)
