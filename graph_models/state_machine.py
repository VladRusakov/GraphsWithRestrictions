from typing import List, Dict


class StateMachine:

    def __init__(self, types: List[str], states: List[str], rules: Dict[str, Dict[str, str]], forbidden: str = 'z'):
        self.states = list(set(states))
        self.forbidden = forbidden
        if self.forbidden in self.states:
            self.states.remove(forbidden)
        self.types = list(set(types))
        pass  # TODO Add rules verification
        self.rules = rules

    def set_rule(self, a: str, b: str, result: str):
        self.check_rule_args(a, b)
        if result == self.forbidden:
            try:
                self.rules[a].pop(b)
            except KeyError:
                pass
            return
        if result not in self.elements:
            raise ValueError(f"Result '{result}' is not included int states set (.elements)")
        if a not in self.rules:
            self.rules[a] = {}
        self.rules[a][b] = result

    def delete_rule(self, a: str, b: str):
        self.set_rule(a, b, self.forbidden)

    def clear_rules(self):
        self.rules.clear()

    def delete_element(self, element: str):
        try:
            self.elements.remove(element)
        except ValueError:
            pass
        try:
            self.rules.pop(element)
        except KeyError:
            pass

    def delete_type(self, type: str):
        try:
            self.types.remove(type)
        except ValueError:
            pass
        for element in self.elements:
            try:
                self.rules[element].pop(type)
            except KeyError:
                pass

    def apply(self, a: str, b: str) -> str:
        self.check_rule_args(a, b)
        return self.forbidden if a == self.forbidden else self.rules[a].get(b, self.forbidden)

    def check_rule_args(self, a: str, b: str):
        if a not in self.elements:
            raise ValueError(f"Element '{a}' is not included into states set (.elements)")
        if b not in self.types:
            raise ValueError(f"Element '{b}' is not included into types set (.types)")
