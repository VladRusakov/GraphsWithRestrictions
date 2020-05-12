from typing import List, Dict
from .cayley_table import CayleyTable


class StateMachine(CayleyTable):

    def __init__(self, types: List[str], elements: List[str], rules: Dict[str, Dict[str, str]], forbidden: str = 'z'):
        super().__init__(elements, rules, forbidden)
        self.types = types

    def apply(self, a: str, b: str) -> str:
        if a not in self.elements:
            raise ValueError(f"Element '{a}' is not included into states set")
        if b not in self.types:
            raise ValueError(f"Element '{b}' is not included into types set")
        return self.forbidden if a == self.forbidden else self.rules[a].get(b, self.forbidden)
