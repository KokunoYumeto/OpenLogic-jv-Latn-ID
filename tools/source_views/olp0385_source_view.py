"""Bounded comparison view for logic-indexed many-valued tautology."""
from __future__ import annotations


def repaired_olp0385_source(text: str) -> str:
    old = r"$\pValue{v}(!A) \in V^+$"
    new = r"$\pValue{v}(!A)[\Log L] \in V^+$"
    assert text.count(old) == 1, text.count(old)
    return text.replace(old, new)
