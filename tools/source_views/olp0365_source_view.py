"""Bounded syntax-chapter identity view for beta-reduction."""
from __future__ import annotations


def repaired_olp0365_source(text: str) -> str:
    repairs = (
        ("% Chapter: introduction", "% Chapter: syntax"),
        (r"\olfileid{lam}{int}{bet}", r"\olfileid{lam}{syn}{bet}"),
    )
    for old, new in repairs:
        assert text.count(old) == 1, (old, text.count(old))
        text = text.replace(old, new)
    return text
