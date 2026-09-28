"""Bounded comparison view for parallel-beta rule and substitution errors."""
from __future__ import annotations


def repaired_olp0369_source(text: str) -> str:
    repairs = (
        (r"$N \xrightarrow{\beta} N'$", r"$N \bredpar N'$"),
        (
            r"\lambd[x][\Subst{N'}{R}{y}]",
            r"\lambd[x][\Subst{N'}{R'}{y}]",
        ),
    )
    for old, new in repairs:
        assert text.count(old) == 1, (old, text.count(old))
        text = text.replace(old, new)
    return text
