"""Bounded comparison view for minimization premise and successor notation."""
from __future__ import annotations


def repaired_olp0355_source(text: str) -> str:
    old_premise = 'Since $f$ is primitive recursive, it is\n!!{lambda defined}'
    new_premise = 'Since $f$ is lambda definable, it is\n!!{lambda defined}'
    assert text.count(old_premise) == 1, text.count(old_premise)
    text = text.replace(old_premise, new_premise)
    old_successor = r'H(S(\num{n}))'
    new_successor = r'H(\fn{Succ}(\num{n}))'
    assert text.count(old_successor) == 3, text.count(old_successor)
    text = text.replace(old_successor, new_successor)
    old_inner = r'h(Sz)'
    new_inner = r'h(\fn{Succ}(z))'
    assert text.count(old_inner) == 1, text.count(old_inner)
    return text.replace(old_inner, new_inner)
