"""Bounded comparison view for parallel beta-eta abstraction premise."""
from __future__ import annotations


def repaired_olp0371_source(text: str) -> str:
    old = r"$N \xrightarrow{\beta} N'$"
    new = r"$N \beredpar N'$"
    assert text.count(old) == 1, text.count(old)
    return text.replace(old, new)
