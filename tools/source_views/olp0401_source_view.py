"""Bounded comparison for invalid nested math delimiters in Gödel negation."""
from __future__ import annotations


def repaired_olp0401_source(text: str) -> str:
    repairs = (
        (r"$1$ & \text{if }", r"1 & \text{if }"),
        (r"$0$ & \text{otherwise}", r"0 & \text{otherwise}"),
    )
    for old, new in repairs:
        assert text.count(old) == 1, (old, text.count(old))
        text = text.replace(old, new)
    return text
