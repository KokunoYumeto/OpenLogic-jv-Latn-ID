"""Bounded comparison view for eta freshness and proof notation.

Only the comparison copy is repaired. The frozen English file remains intact.
"""
from __future__ import annotations


def repaired_olp0366_source(text: str) -> str:
    repairs = (
        (
            r"\lambd[x][f x] \equal f",
            r"\lambd[x][f x] \equal f \text{ yen } x \notin FV(f)",
        ),
        ("$ext$ rule", r"$\ext$ rule"),
        (r"$M" + "\n" + r"  \equal N$ derived by the \ext{} rule",
         r"$M" + "\n" + r"  \equal[\ext] N$ derived by the \ext{} rule"),
        (r"$\equal[ext]$", r"$\equal[\ext]$"),
    )
    for old, new in repairs:
        assert text.count(old) == 1, (old, text.count(old))
        text = text.replace(old, new)
    return text
