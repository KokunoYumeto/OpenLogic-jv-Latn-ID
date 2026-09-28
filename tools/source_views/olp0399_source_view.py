"""Bounded comparison for rational-value denominator and finite-grid bounds."""
from __future__ import annotations


def repaired_olp0399_source(text: str) -> str:
    repairs = (
        (
            r"n,m \in \Nat \text{ and } n\le m",
            r"n,m \in \Nat, 0<m, n\le m",
        ),
        (
            r"n \in \Nat \text{ and } n\le m",
            r"n \in \Nat \text{ lan } n<m",
        ),
    )
    for old, new in repairs:
        assert text.count(old) == 1, (old, text.count(old))
        text = text.replace(old, new)
    return text
