"""Bounded comparison view for the indexed constant-function equation."""
from __future__ import annotations


def repaired_olp0374_source(text: str) -> str:
    old = r"$c(n) = k$"
    new = r"$c_k(n) = k$"
    assert text.count(old) == 1, text.count(old)
    return text.replace(old, new)
