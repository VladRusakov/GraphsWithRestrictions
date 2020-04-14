from typing import Dict, List


class CayleyTable:

    def __init__(self, elements: List[str], rules: Dict[str, Dict[str, str]], forbidden: str = 'z'):
        self.elements = elements
        self.forbidden = forbidden
        self.rules = rules

    def apply(self, a: str, b: str) -> str:
        if a not in self.elements:
            raise ValueError(f"Element '{a}' is not included into elements set")
        if b not in self.elements:
            raise ValueError(f"Element '{b}' is not included into elements set")

        return self.rules[a].get(b, self.forbidden)
