"""Bounded comparison view for the unary zero function."""
from __future__ import annotations


def repaired_olp0351_source(text: str) -> str:
    old = r'\lambd[x][\lambd[y][y]]'
    new = r'\lambd[u][\lambd[x][\lambd[y][y]]]'
    assert text.count(old) == 1, text.count(old)
    return text.replace(old, new)
