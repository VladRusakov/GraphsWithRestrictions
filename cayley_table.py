from typing import Dict, Set


class CayleyTable:

    def __init__(self, alphabet: Set[str], forbidden: str, rules: Dict[str, Dict[str, str]]):
        self.alphabet = alphabet
        self.forbidden = forbidden
        self.rules = rules

    def apply(self, a: str, b: str) -> str:
        if not set(a, b).issubset(self.alphabet):
            raise ValueError
        return self.rules[a][b]
