from typing import List, Any, Dict

from graph_models.state_machine import StateMachine
from ui.utils.model import Observable, update_observers


class MachineWindowModel(Observable):

    @update_observers
    def __init__(self):
        super().__init__()
        self.machine = StateMachine([], [], {})

    @update_observers
    def change_rule(self, state: str, arc_type: str, result: str):
        self.machine.set_rule(state, arc_type, result)

    @update_observers
    def update_states(self, new_states: List[str]):
        removable_states = set(self.machine.states).difference(new_states)
        for state in removable_states:
            self.machine.remove_state(state)
        for state in new_states:
            if state not in self.machine.states:
                self.machine.add_state(state)

    @update_observers
    def update_types(self, new_types: List[str]):
        removable_types = set(self.machine.types).difference(new_types)
        for arc_type in removable_types:
            self.machine.remove_type(arc_type)
        for arc_type in new_types:
            if arc_type not in self.machine.types:
                self.machine.add_type(arc_type)

    @update_observers
    def update_forbidden(self, new_forbidden: str):
        self.machine.forbidden = new_forbidden

    @update_observers
    def rename_state(self, state: str, new_state: str):
        self.machine.rename_state(state, new_state)

    @update_observers
    def rename_type(self, arc_type, new_type):
        self.machine.rename_type(arc_type, new_type)

    @update_observers
    def set_rule(self, state, arc_type, result):
        self.machine.set_rule(state, arc_type, result)

    @update_observers
    def clear_machine(self):
        self.machine.remove_all_states()
        self.machine.remove_all_types()
        self.update_forbidden(None)

    def save_machine(self, path: str):
        with open(path, 'wb') as file:
            file.write(str(self.machine).encode())

    @update_observers
    def read_machine(self, path: str) -> Dict[str, Any]:
        with open(path, 'rb') as file:
            from ast import literal_eval
            lines = [line.decode().strip() for line in file]
            attrs = {}
            index = 0
            while not lines[index].startswith('rules'):
                index += 1
            lines[index] = str.join('', lines[index:])
            lines = lines[:index+1]
            for line in lines:
                field, data = line.split(':', maxsplit=1)
                attrs[field.strip()] = literal_eval(data.strip())

            self.machine = StateMachine(**attrs)
