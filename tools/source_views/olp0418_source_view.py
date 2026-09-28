"""Bounded comparison for ordered-triple countermodel notation."""
from __future__ import annotations


def repaired_olp0418_source(text: str) -> str:
    old = r"\mModel{M'} =" + "\n  " + r"\{W', R', V'\}"
    new = r"\mModel{M'} =" + "\n  " + r"\tuple{W', R', V'}"
    assert text.count(old) == 1, (old, text.count(old))
    return text.replace(old, new)
