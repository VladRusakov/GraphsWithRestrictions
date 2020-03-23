from typing import Dict, Set


class CayleyTable:

    def __init__(self, monoid: Set[str], forbidden: str, rules: Dict[str, Dict[str, str]]):
        self.monoid = monoid
        self.forbidden = forbidden
        self.rules = rules

    def apply(self, a: str, b: str) -> str:
        if not set(a, b).issubset(self.monoid):
            raise ValueError('Element is not included into monoid')
        return self.rules[a][b]
