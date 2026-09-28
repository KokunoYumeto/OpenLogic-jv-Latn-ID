"""Bounded comparison view for Church--Rosser proof endpoint subscripts."""
from __future__ import annotations


def repaired_olp0368_source(text: str) -> str:
    repairs = (
        (r"$N_{m,0}$ is $P$", r"$N_{m,0}$ is $P_m$"),
        (r"$N_{0,n}$" + "\n" + r"  is $Q$", r"$N_{0,n}$" + "\n" + r"  is $Q_n$"),
    )
    for old, new in repairs:
        assert text.count(old) == 1, (old, text.count(old))
        text = text.replace(old, new)
    return text
