from graph_models.state_machine import StateMachine


def generate_machine_mixed_simple() -> StateMachine:

    reset, setup = 'a', 'b'
    zero_level, first_level, forbidden = 'e', 'b', 'z'

    elements = [zero_level, first_level, forbidden]
    types = [reset, setup]

    rules = {}
    rules[zero_level].update({reset: zero_level, setup: first_level})
    rules[first_level].update({reset: zero_level, setup: forbidden})

    return StateMachine(types, elements, rules, forbidden)
