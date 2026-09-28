"""Bounded comparison view for the eta one-step case."""
from __future__ import annotations


def repaired_olp0372_source(text: str) -> str:
    old = r"If $M \bredone" + "\n" + r"  M'$ by $\eta$-conversion"
    new = r"If $M \eredone" + "\n" + r"  M'$ by $\eta$-conversion"
    assert text.count(old) == 1, text.count(old)
    return text.replace(old, new)
