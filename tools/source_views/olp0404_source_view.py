"""Bounded comparison for indexed sequent side and logic-indexed nonderivability."""
from __future__ import annotations


def repaired_olp0404_source(text: str) -> str:
    repairs = (
        (r"where each $\Gamma_1$", r"where each $\Gamma_i$"),
        (r"$\Gamma \Proves/ !A$", r"$\Gamma \Proves/[\Log{L}] !A$"),
    )
    for old, new in repairs:
        assert text.count(old) == 1, (old, text.count(old))
        text = text.replace(old, new)
    return text
