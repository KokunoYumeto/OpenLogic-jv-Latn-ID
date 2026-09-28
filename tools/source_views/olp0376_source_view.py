"""Bounded comparison view for the Church-zero predecessor state."""
from __future__ import annotations


def repaired_olp0376_source(text: str) -> str:
    old = r"$\tuple{0,0}$"
    new = r"$\tuple{\num 0,\num 0}$"
    assert text.count(old) == 2, text.count(old)
    return text.replace(old, new)
