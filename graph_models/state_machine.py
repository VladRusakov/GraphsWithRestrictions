from typing import List, Dict


class StateMachine:

    def __init__(self, states: List[str], types: List[str], rules: Dict[str, Dict[str, str]], forbidden: str = 'z'):
        self.states = list(set(states))
        self.forbidden = forbidden
        if self.forbidden in self.states:
            self.states.remove(forbidden)
        self.types = list(set(types))
        pass  # TODO Add rules verification
        self.rules = rules

    def add_state(self, new_state: str):
        if new_state not in self.states and new_state != self.forbidden:
            self.states.append(new_state)

    def rename_state(self, old_state: str, new_state: str):
        if new_state == self.forbidden:
            self.remove_state(old_state)

        elif old_state in self.states:
            if new_state in self.states:
                self.remove_state(old_state)
            else:
                state_index = self.states.index(old_state)
                self.states[state_index] = new_state
                try:
                    state_rules = self.rules.pop(old_state)
                    self.rules[new_state] = state_rules
                except KeyError:
                    pass
        else:
            pass  # TODO raise exception?

    def remove_state(self, state: str):
        try:
            self.states.remove(state)
        except ValueError:
            pass
        try:
            self.rules.pop(state)
        except KeyError:
            pass

    def remove_all_states(self):
        self.states.clear()
        self.remove_all_rules()

    def add_type(self, new_type: str):
        if new_type not in self.types:
            self.types.append(new_type)

    def rename_type(self, old_type: str, new_type: str):
        if old_type in self.types:
            if new_type in self.types:
                self.remove_type(new_type)
            self.types.append(new_type)
            for state in self.states:
                try:
                    rule_result = self.rules[state].pop(old_type)
                    self.rules[state][new_type] = rule_result
                except KeyError:
                    pass
        else:
            raise ValueError(f"'{old_type}' not in types")

    def remove_type(self, removed_type: str):
        try:
            self.types.remove(removed_type)
        except ValueError:
            pass
        for state in self.states:
            try:
                self.rules[state].pop(removed_type)
            except KeyError:
                pass

    def remove_all_types(self):
        self.types.clear()
        self.remove_all_rules()

    def rename_forbidden(self, new_forbidden):
        if new_forbidden in self.states:
            self.remove_state(new_forbidden)
        self.forbidden = new_forbidden

    def apply(self, a: str, b: str) -> str:
        self.check_rule_args(a, b)
        return self.forbidden if a == self.forbidden else self.rules[a].get(b, self.forbidden)

    def set_rule(self, a: str, b: str, result: str):
        self.check_rule_args(a, b)
        if result == self.forbidden:
            try:
                self.rules[a].pop(b)
            except KeyError:
                pass
            return
        if result not in self.states:
            raise ValueError(f"Result '{result}' is not included int states set (.states)")
        if a not in self.rules:
            self.rules[a] = {}
        self.rules[a][b] = result

    def remove_rule(self, a: str, b: str):
        self.set_rule(a, b, self.forbidden)

    def remove_all_rules(self):
        self.rules.clear()

    def check_rule_args(self, a: str, b: str):
        if a not in self.states or a != self.forbidden:
            raise ValueError(f"Element '{a}' is not included into states set (.states) or forbidden")
        if b not in self.types:
            raise ValueError(f"Element '{b}' is not included into types set (.types)")
