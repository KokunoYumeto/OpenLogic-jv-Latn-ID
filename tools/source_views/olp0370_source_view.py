"""Bounded comparison view for the mislabeled proof-case body term."""
from __future__ import annotations


def repaired_olp0370_source(text: str) -> str:
    old = r"$N$, $M'$, $Q$, $Q'$, where"
    new = r"$N$, $N'$, $Q$, $Q'$, where"
    assert text.count(old) == 1, text.count(old)
    return text.replace(old, new)
