"""Bounded comparison view for implication introduction's conclusion."""


def repaired_olp0663_source(s: str) -> str:
    wrong = r"then $\Gamma \Entails !B$"
    right = r"then $\Gamma \Entails !A \lif !B$"
    assert s.count(wrong) == 1, s.count(wrong)
    return s.replace(wrong, right, 1)
