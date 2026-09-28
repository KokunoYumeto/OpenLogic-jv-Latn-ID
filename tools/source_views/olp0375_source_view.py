"""Bounded comparison view for chapter comment and multiplication exercise."""
from __future__ import annotations


def repaired_olp0375_source(text: str) -> str:
    repairs = (
        ("% Chapter: lambda-definablity", "% Chapter: lambda-definability"),
        (
            r"\fn{Mult}' \ident \lambd[ab][a (\fn{Add}\, a) \num{0}].",
            r"\fn{Mult}' \ident \lambd[ab][a (\fn{Add}\, b) \num{0}].",
        ),
    )
    for old, new in repairs:
        assert text.count(old) == 1, (old, text.count(old))
        text = text.replace(old, new)
    return text
