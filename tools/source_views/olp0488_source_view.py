"""Bounded comparison view for the bisimulation agent and relation indices."""


def repaired_olp0488_source(s: str) -> str:
    old = r"agents $a \in A$"
    new = r"agents $a \in G$"
    assert s.count(old) == 2
    assert s.count(r"R_{1_a}") == s.count(r"R_{2_a}") == 2
    return (s.replace(old, new)
             .replace(r"R_{1_a}", r"R_{1,a}")
             .replace(r"R_{2_a}", r"R_{2,a}"))
