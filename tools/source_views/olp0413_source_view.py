"""Bounded comparison for omitted world index in duality proof."""
from __future__ import annotations


def repaired_olp0413_source(text: str) -> str:
    old = r"$\mSat/{M}{\Box\lnot !A}$"
    new = r"$\mSat/{M}{\Box\lnot !A}[w]$"
    assert text.count(old) == 1, (old, text.count(old))
    return text.replace(old, new)
