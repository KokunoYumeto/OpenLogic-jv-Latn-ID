"""Bounded comparison view for relation arity in truth-value encoding."""
from __future__ import annotations


def repaired_olp0377_source(text: str) -> str:
    old = r"$R \subseteq \Nat^n$"
    new = r"$R \subseteq \Nat^k$"
    assert text.count(old) == 1, text.count(old)
    return text.replace(old, new)
